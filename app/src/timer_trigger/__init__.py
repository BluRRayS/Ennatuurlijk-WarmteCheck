import logging
import azure.functions as func
from ..main import run_and_upload
from ..services import OpenMeteoWeatherService


def main(_: func.TimerRequest) -> None:
    logging.info("Timer triggered WarmteCheck")
    try:
        # Use the OpenMeteo service
        weather_service = OpenMeteoWeatherService()
        run_and_upload(weather_service)
    except Exception as e:
        logging.exception("WarmteCheck failed: %s", e)
