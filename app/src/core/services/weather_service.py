from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import requests
from src.config import WeatherConfig

class WeatherServiceInterface(ABC):
    """Abstract interface for weather services."""
    
    @abstractmethod
    def fetch_hourly_forecast(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Fetch the 24-hour temperature forecast for given coordinates.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            A list of hourly forecast data, with each item containing 'time' and 'temp'.
        """
        pass

class OpenMeteoWeatherService(WeatherServiceInterface):
    """Weather service implementation using OpenMeteo API."""
    
    def __init__(self, config: WeatherConfig):
        self.config = config
    
    def fetch_hourly_forecast(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Fetch 24-hour temperature forecast from OpenMeteo API."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m",
            "forecast_days": 1
        }
        response = requests.get(
            self.config.api_base_url, 
            params=params,
            timeout=self.config.timeout_seconds
        )
        response.raise_for_status()
        data = response.json()
        
        hourly_data = data.get("hourly", {})
        times = hourly_data.get("time", [])
        temperatures = hourly_data.get("temperature_2m", [])
        
        forecast = [
            {"time": time, "temp": temp}
            for time, temp in zip(times, temperatures)
        ]
        return forecast


class MockWeatherService(WeatherServiceInterface):
    """Mock weather service for testing purposes."""
    
    def __init__(self, mock_forecast: Optional[List[Dict[str, Any]]] = None):
        if mock_forecast is None:
            self.mock_forecast: List[Dict[str, Any]] = [{"time": "2023-01-01T12:00", "temp": 15.0}]
        else:
            self.mock_forecast = mock_forecast
        self.call_count = 0
        self.last_coordinates: Dict[str, Any] = {}
    
    def fetch_hourly_forecast(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Return mock forecast and track calls for testing."""
        self.call_count += 1
        self.last_coordinates = {"lat": lat, "lon": lon}
        return self.mock_forecast
    
    def set_forecast(self, forecast: List[Dict[str, Any]]) -> None:
        """Set the mock forecast to return."""
        self.mock_forecast = forecast
