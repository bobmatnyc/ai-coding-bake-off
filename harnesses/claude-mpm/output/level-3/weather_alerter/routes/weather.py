"""Weather data endpoint."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from weather_alerter.database import get_db
from weather_alerter.weather_client import get_weather

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/{city_id}")
def get_city_weather(
    city_id: int,
    db: sqlite3.Connection = Depends(get_db),
) -> dict:
    """Fetch current weather data for a city."""
    city = db.execute("SELECT * FROM cities WHERE id = ?", (city_id,)).fetchone()
    if city is None:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")

    try:
        weather_data = get_weather(city["latitude"], city["longitude"])
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Weather API error: {exc}",
        ) from exc

    return {
        "city_id": city_id,
        "city_name": city["name"],
        **weather_data,
    }
