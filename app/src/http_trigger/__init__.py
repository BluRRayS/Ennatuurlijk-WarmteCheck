import json
from typing import List
import azure.functions as func

from src.core.main import run_and_upload
from src.core.services.weather_service import OpenMeteoWeatherService
from src.core.services.storage_service import AzureBlobStorageService
from src.core.config import get_app_config
from src.core.models.location import Location


def main(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function for WarmteCheck."""
    try:
        app_config = get_app_config()

        # Get locations from request body or config
        if req.get_body():
            try:
                locations: List[Location] = req.get_json()
            except ValueError:
                return func.HttpResponse("Invalid JSON in request body.", status_code=400)
        else:
            try:
                locations = app_config.locations
            except json.JSONDecodeError:
                return func.HttpResponse("Failed to parse LOCATIONS_JSON from config.", status_code=500)

        # Setup services based on config
        weather_service = OpenMeteoWeatherService(app_config.weather)
        storage_service = AzureBlobStorageService(app_config.storage)

        # Execute the main logic
        output_data = run_and_upload(weather_service, storage_service, locations)

        return func.HttpResponse(
            body=json.dumps(output_data),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(body=str(e), status_code=500)