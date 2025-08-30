from abc import ABC, abstractmethod
from typing import Dict, Any
import requests


class WeatherServiceInterface(ABC):
    """Abstract interface for weather services."""
    
    @abstractmethod
    def fetch_temperature(self, lat: float, lon: float) -> float:
        """Fetch the current temperature for given coordinates.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            Current temperature in Celsius
        """
        pass


class OpenMeteoWeatherService(WeatherServiceInterface):
    """Weather service implementation using OpenMeteo API."""
    
    def __init__(self, api_url: str = "https://api.open-meteo.com/v1/forecast"):
        self.api_url = api_url
    
    def fetch_temperature(self, lat: float, lon: float) -> float:
        """Fetch temperature from OpenMeteo API."""
        response = requests.get(
            self.api_url, 
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            }, 
            timeout=10
        )
        response.raise_for_status()
        return response.json()["current_weather"]["temperature"]


class MockWeatherService(WeatherServiceInterface):
    """Mock weather service for testing purposes."""
    
    def __init__(self, mock_temperature: float = 15.0):
        self.mock_temperature = mock_temperature
        self.call_count = 0
        self.last_coordinates: Dict[str, Any] = {}
    
    def fetch_temperature(self, lat: float, lon: float) -> float:
        """Return mock temperature and track calls for testing."""
        self.call_count += 1
        self.last_coordinates = {"lat": lat, "lon": lon}
        return self.mock_temperature
    
    def set_temperature(self, temperature: float) -> None:
        """Set the mock temperature to return."""
        self.mock_temperature = temperature
