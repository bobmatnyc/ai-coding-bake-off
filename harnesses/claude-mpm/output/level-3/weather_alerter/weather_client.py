"""OpenWeatherMap API client with mock mode support."""

import os

import httpx

MOCK_WEATHER: dict = {
    "main": {"temp": 22.5, "feels_like": 21.8, "humidity": 65, "pressure": 1013},
    "wind": {"speed": 4.12, "deg": 250},
    "weather": [{"main": "Clear", "description": "clear sky"}],
    "name": "Mock City",
}


def get_weather(lat: float, lon: float) -> dict:
    """Fetch current weather for given coordinates.

    Returns mock data if OPENWEATHERMAP_API_KEY is not set or
    WEATHER_MOCK_MODE=true is configured.

    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.

    Returns:
        Dictionary with weather data in OpenWeatherMap format.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
    mock_mode = os.getenv("WEATHER_MOCK_MODE", "false").lower() == "true"

    if not api_key or mock_mode:
        return MOCK_WEATHER

    response = httpx.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
