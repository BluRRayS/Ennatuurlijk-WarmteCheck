import os
from dataclasses import dataclass
from typing import List, Optional

from app.src.core.models.location import Location

@dataclass
class WeatherConfig:
    api_base_url: str = "https://api.open-meteo.com/v1/forecast"
    timeout_seconds: int = 10

@dataclass
class StorageConfig:
    storage_type: str = "local"  # "local" or "azure_blob"
    local_storage_path: str = "./output"
    account_name: Optional[str] = None
    container_name: str = "warmtecheck"

@dataclass
class AppConfig:
    weather: WeatherConfig
    storage: StorageConfig
    locations: List[Location]


def load_env_file(file_path: str = ".env") -> None:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def get_app_config() -> AppConfig:
    load_env_file()
    
    weather_config = WeatherConfig(
        api_base_url=os.getenv("WEATHER_API_BASE_URL", "https://api.open-meteo.com/v1/forecast"),
        timeout_seconds=int(os.getenv("WEATHER_API_TIMEOUT", "10"))
    )
    
    storage_config = StorageConfig(
        storage_type=os.getenv("STORAGE_TYPE", "local"),
        local_storage_path=os.getenv("LOCAL_STORAGE_PATH", "./output"),
        account_name=os.getenv("STORAGE_ACCOUNT_NAME"),
        container_name=os.getenv("STORAGE_CONTAINER", "warmtecheck"),
    )

    default_locations = [Location(name="Eindhoven", lat=51.44, lon=5.47)]

    return AppConfig(
        weather=weather_config,
        storage=storage_config,
        locations=default_locations
    )
