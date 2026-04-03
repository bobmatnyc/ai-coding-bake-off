"""Alert log endpoints."""

import sqlite3
from typing import Optional

from fastapi import APIRouter, Depends, Query

from weather_alerter.database import get_db
from weather_alerter.models import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


def _row_to_alert(row: sqlite3.Row) -> AlertResponse:
    return AlertResponse(
        id=row["id"],
        city_id=row["city_id"],
        threshold_id=row["threshold_id"],
        triggered_at=row["triggered_at"],
        metric_value=row["metric_value"],
        message=row["message"],
    )


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    city_id: Optional[int] = Query(None, description="Filter alerts by city ID"),
    db: sqlite3.Connection = Depends(get_db),
) -> list[AlertResponse]:
    """List all alerts, optionally filtered by city."""
    if city_id is not None:
        rows = db.execute(
            "SELECT * FROM alert_log WHERE city_id = ? ORDER BY id", (city_id,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM alert_log ORDER BY id").fetchall()
    return [_row_to_alert(r) for r in rows]
