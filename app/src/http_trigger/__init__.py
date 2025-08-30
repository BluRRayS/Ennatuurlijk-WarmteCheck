import json
import azure.functions as func

from ..main import run_and_upload, create_weather_service, create_storage_service
from ..config import get_app_config


def main(_: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function for WarmteCheck.
    
    Args:
        req: HTTP request object
        
    Returns:
        HTTP response with weather data JSON
    """
    try:
        config = get_app_config()
        weather_service = create_weather_service(config)
        storage_service = create_storage_service(config)
        out = run_and_upload(weather_service, storage_service, config)
        
        return func.HttpResponse(
            body=json.dumps(out), 
            status_code=200, 
            mimetype="application/json"
        )
            
    except Exception as e:
        return func.HttpResponse(body=str(e), status_code=500)