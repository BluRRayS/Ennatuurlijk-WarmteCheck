"""Location model and related constants for WarmteCheck application."""

from typing import List, TypedDict


class Location(TypedDict):
    """Location data structure with name and coordinates."""
    name: str
    lat: float
    lon: float


# Default locations for temperature monitoring
DEFAULT_PLACES: List[Location] = [
    {"name": "Eindhoven", "lat": 51.4416, "lon": 5.4697},
    {"name": "Utrecht", "lat": 52.0907, "lon": 5.1214},
]
