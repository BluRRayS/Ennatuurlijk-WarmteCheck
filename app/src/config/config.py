"""Configuration management for the WarmteCheck application."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherConfig:
    """Configuration for weather service."""
    api_base_url: str = "https://api.open-meteo.com/v1/forecast"
    timeout_seconds: int = 10


@dataclass
class StorageConfig:
    """Configuration for storage service."""
    storage_type: str = "local"  # "local" or "azure_blob"
    local_storage_path: str = "./"
    azure_storage_account: Optional[str] = None
    azure_container_name: str = "warmtecheck"
    output_filename: str = "latest.json"


@dataclass
class AppConfig:
    """Main application configuration."""
    weather: WeatherConfig
    storage: StorageConfig


def load_env_file(file_path: str = ".env") -> None:
    """Load environment variables from a file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def get_app_config() -> AppConfig:
    """Get application configuration from environment variables."""
    # Load .env file if it exists
    load_env_file()
    
    weather_config = WeatherConfig(
        api_base_url=os.getenv("WEATHER_API_BASE_URL", "https://api.open-meteo.com/v1/forecast"),
        timeout_seconds=int(os.getenv("WEATHER_API_TIMEOUT", "10"))
    )
    
    storage_config = StorageConfig(
        storage_type=os.getenv("STORAGE_TYPE", "local"),
        local_storage_path=os.getenv("LOCAL_STORAGE_PATH", "./"),
        azure_storage_account=os.getenv("STORAGE_ACCOUNT_NAME"),
        azure_container_name=os.getenv("STORAGE_CONTAINER", "warmtecheck"),
        output_filename=os.getenv("OUTPUT_BLOB", "latest.json")
    )
    
    return AppConfig(
        weather=weather_config,
        storage=storage_config
    )
