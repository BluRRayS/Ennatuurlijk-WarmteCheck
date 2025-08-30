import logging
import datetime
import azure.functions as func

from src.main import run_and_upload
from src.services.weather_service import OpenMeteoWeatherService
from src.services.storage_service import LocalStorageService
from src.config import get_app_config


def main(timer: func.TimerRequest) -> None:
    try:
        utc_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        logging.info("Timer triggered WarmteCheck at %s", utc_timestamp)
        
        app_config = get_app_config()
        locations = app_config.locations

        weather_service = OpenMeteoWeatherService(app_config.weather)
        storage_service = LocalStorageService(app_config.storage.local_storage_path)

        run_and_upload(weather_service, storage_service, locations)

        logging.info("WarmteCheck finished successfully.")

    except Exception as e:
        logging.exception(f"WarmteCheck failed: {e}")
