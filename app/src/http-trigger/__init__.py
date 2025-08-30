import json
import azure.functions as func

from ..main import run_and_upload
from ..weather_service import OpenMeteoWeatherService


def main(_: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function for WarmteCheck.
    
    Args:
        req: HTTP request object
        
    Returns:
        HTTP response with weather data JSON
    """
    try:
        weather_service = OpenMeteoWeatherService()
        out = run_and_upload(weather_service)
        
        return func.HttpResponse(
            body=json.dumps(out), 
            status_code=200, 
            mimetype="application/json"
        )
            
    except Exception as e:
        return func.HttpResponse(body=str(e), status_code=500)