"""Threshold management endpoints."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from weather_alerter.database import get_db
from weather_alerter.models import ThresholdCreate, ThresholdResponse

router = APIRouter(tags=["thresholds"])


def _row_to_threshold(row: sqlite3.Row) -> ThresholdResponse:
    return ThresholdResponse(
        id=row["id"],
        city_id=row["city_id"],
        metric=row["metric"],
        operator=row["operator"],
        value=row["value"],
        enabled=bool(row["enabled"]),
    )


@router.post("/cities/{city_id}/thresholds", status_code=201, response_model=ThresholdResponse)
def create_threshold(
    city_id: int,
    payload: ThresholdCreate,
    db: sqlite3.Connection = Depends(get_db),
) -> ThresholdResponse:
    """Add a threshold to a city."""
    city = db.execute("SELECT id FROM cities WHERE id = ?", (city_id,)).fetchone()
    if city is None:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")

    cursor = db.execute(
        """
        INSERT INTO thresholds (city_id, metric, operator, value, enabled)
        VALUES (?, ?, ?, ?, ?)
        """,
        (city_id, payload.metric, payload.operator, payload.value, int(payload.enabled)),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM thresholds WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return _row_to_threshold(row)


@router.get("/cities/{city_id}/thresholds", response_model=list[ThresholdResponse])
def list_thresholds(
    city_id: int,
    db: sqlite3.Connection = Depends(get_db),
) -> list[ThresholdResponse]:
    """List all thresholds for a city."""
    city = db.execute("SELECT id FROM cities WHERE id = ?", (city_id,)).fetchone()
    if city is None:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")

    rows = db.execute(
        "SELECT * FROM thresholds WHERE city_id = ? ORDER BY id", (city_id,)
    ).fetchall()
    return [_row_to_threshold(r) for r in rows]


@router.delete("/thresholds/{threshold_id}", status_code=204)
def delete_threshold(
    threshold_id: int,
    db: sqlite3.Connection = Depends(get_db),
) -> None:
    """Delete a threshold by ID."""
    row = db.execute(
        "SELECT id FROM thresholds WHERE id = ?", (threshold_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Threshold {threshold_id} not found")
    db.execute("DELETE FROM thresholds WHERE id = ?", (threshold_id,))
    db.commit()
