from datetime import datetime, timezone
from typing import List, Dict, Any
from src.core.services.storage_service import StorageServiceInterface
from src.core.services.weather_service import WeatherServiceInterface
from src.core.models.location import Location


def calculate_heating_index(temp_c: float) -> float:
    """Calculate heating index based on temperature in Celsius.
    
    Args:
        temp_c: Temperature in Celsius
        
    Returns:
        Heating index (how much heating is needed, 0 if temp >= 20°C)
    """
    return max(0.0, 20.0 - temp_c)


def get_hourly_forecast_for_given_locations(
    weather_service: WeatherServiceInterface, 
    locations: List[Location]
) -> Dict[str, Any]:
    """Get 24-hour temperature forecast for given locations and calculate heating indices.
    
    Args:
        weather_service: Service to fetch weather data
        locations: List of locations with name, lat, lon
        
    Returns:
        Dictionary with generated timestamp and results for each location
    """
    results: List[Dict[str, Any]] = []
    for location in locations:
        forecast_data = weather_service.fetch_hourly_forecast(location["lat"], location["lon"])
        
        hourly_heating_indices = [
            {
                "time": entry["time"],
                "temp": entry["temp"],
                "heating_index": calculate_heating_index(entry["temp"])
            }
            for entry in forecast_data
        ]
        
        results.append({
            "place": location["name"],
            "forecast": hourly_heating_indices
        })
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "results": results}

def run_and_upload(
    weather_service: WeatherServiceInterface, 
    storage_service: StorageServiceInterface,
    locations: List[Location]
) -> None:
    payload = get_hourly_forecast_for_given_locations(weather_service, locations)
    storage_service.upload(payload)