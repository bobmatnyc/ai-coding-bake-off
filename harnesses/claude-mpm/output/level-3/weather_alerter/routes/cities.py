"""City management endpoints."""

import sqlite3
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from weather_alerter.database import get_db
from weather_alerter.models import CityCreate, CityResponse, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


def _row_to_city(row: sqlite3.Row) -> CityResponse:
    return CityResponse(
        id=row["id"],
        name=row["name"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        enabled=bool(row["enabled"]),
        created_at=row["created_at"],
    )


@router.post("", status_code=201, response_model=CityResponse)
def create_city(
    payload: CityCreate,
    db: sqlite3.Connection = Depends(get_db),
) -> CityResponse:
    """Create a new city for weather monitoring."""
    now = datetime.now(timezone.utc).isoformat()
    cursor = db.execute(
        """
        INSERT INTO cities (name, latitude, longitude, enabled, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (payload.name, payload.latitude, payload.longitude, int(payload.enabled), now),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM cities WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return _row_to_city(row)


@router.get("", response_model=dict)
def list_cities(
    db: sqlite3.Connection = Depends(get_db),
) -> dict:
    """List all cities."""
    rows = db.execute("SELECT * FROM cities ORDER BY id").fetchall()
    return {"cities": [_row_to_city(r).model_dump() for r in rows]}


@router.get("/{city_id}", response_model=CityResponse)
def get_city(
    city_id: int,
    db: sqlite3.Connection = Depends(get_db),
) -> CityResponse:
    """Get a single city by ID."""
    row = db.execute("SELECT * FROM cities WHERE id = ?", (city_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")
    return _row_to_city(row)


@router.patch("/{city_id}", response_model=CityResponse)
def update_city(
    city_id: int,
    payload: CityUpdate,
    db: sqlite3.Connection = Depends(get_db),
) -> CityResponse:
    """Partially update a city."""
    row = db.execute("SELECT * FROM cities WHERE id = ?", (city_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")

    updates: dict = {}
    if payload.name is not None:
        updates["name"] = payload.name
    if payload.latitude is not None:
        updates["latitude"] = payload.latitude
    if payload.longitude is not None:
        updates["longitude"] = payload.longitude
    if payload.enabled is not None:
        updates["enabled"] = int(payload.enabled)

    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [city_id]
        db.execute(f"UPDATE cities SET {set_clause} WHERE id = ?", values)
        db.commit()

    updated = db.execute("SELECT * FROM cities WHERE id = ?", (city_id,)).fetchone()
    return _row_to_city(updated)


@router.delete("/{city_id}", status_code=204)
def delete_city(
    city_id: int,
    db: sqlite3.Connection = Depends(get_db),
) -> None:
    """Delete a city and all its thresholds."""
    row = db.execute("SELECT id FROM cities WHERE id = ?", (city_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")
    db.execute("DELETE FROM cities WHERE id = ?", (city_id,))
    db.commit()
