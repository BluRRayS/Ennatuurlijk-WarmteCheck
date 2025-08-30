import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, TypedDict

# Azure identity + blob client
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Local imports
from .weather_service import WeatherServiceInterface, OpenMeteoWeatherService


class Location(TypedDict):
    name: str
    lat: float
    lon: float


PLACES: List[Location] = [
    {"name": "Eindhoven", "lat": 51.4416, "lon": 5.4697},
    {"name": "Utrecht", "lat": 52.0907, "lon": 5.1214},
]


def calculate_heating_index(temp_c: float) -> float:
    """Calculate heating index based on temperature in Celsius.
    
    Args:
        temp_c: Temperature in Celsius
        
    Returns:
        Heating index (how much heating is needed, 0 if temp >= 20°C)
    """
    return max(0.0, 20.0 - temp_c)


def get_temperature_forecast_for_given_locations_in_celcius(
    weather_service: WeatherServiceInterface, 
    locations: List[Location]
) -> Dict[str, Any]:
    """Get temperature forecast for given locations and calculate heating indices.
    
    Args:
        weather_service: Service to fetch weather data
        locations: List of locations with name, lat, lon
        
    Returns:
        Dictionary with generated timestamp and results for each location
    """
    results: List[Dict[str, Any]] = []
    for location in locations:
        temp = weather_service.fetch_temperature(location["lat"], location["lon"])
        results.append({
            "place": location["name"], 
            "temp": temp, 
            "heating_index": calculate_heating_index(temp)
        })
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "results": results}

def upload_to_blob(payload: Dict[str, Any]) -> None:
    # Prefer managed identity in Azure (DefaultAzureCredential). Locally, you can use AZURE_STORAGE_CONNECTION_STRING env var.
    storage_account = os.environ.get("STORAGE_ACCOUNT_NAME")
    container = os.environ.get("STORAGE_CONTAINER", "warmtecheck")
    blob_name = os.environ.get("OUTPUT_BLOB", "latest.json")

    if storage_account:
        account_url = f"https://{storage_account}.blob.core.windows.net"
        if DefaultAzureCredential and BlobServiceClient:
            cred = DefaultAzureCredential()
            client = BlobServiceClient(account_url=account_url, credential=cred)
            container_client = client.get_container_client(container)
            try:
                container_client.create_container()
            except Exception:
                pass
            container_client.get_blob_client(blob_name).upload_blob(json.dumps(payload), overwrite=True)
        else:
            raise ImportError("Azure SDK packages not available")
    else:
        # local fallback: write to file
        with open(blob_name, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

def run_and_upload(weather_service: WeatherServiceInterface) -> Dict[str, Any]:
    """Run temperature collection and upload results to blob storage.
    
    Args:
        weather_service: Service to fetch weather data
        
    Returns:
        Dictionary with temperature and heating index data for all locations
    """
    payload = get_temperature_forecast_for_given_locations_in_celcius(weather_service, PLACES)
    upload_to_blob(payload)
    return payload

if __name__ == "__main__":
    print("Running local WarmteCheck")
    weather_service = OpenMeteoWeatherService()
    out = run_and_upload(weather_service)
    print("Output written:", out)
