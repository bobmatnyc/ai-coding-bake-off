"""Alert evaluation logic for weather threshold monitoring."""

import sqlite3
from datetime import datetime, timezone

from weather_alerter.database import get_connection


def check_threshold(
    weather_data: dict,
    metric: str,
    operator: str,
    value: float,
) -> bool:
    """Check whether a weather metric exceeds a threshold.

    Args:
        weather_data: Weather data dict in OpenWeatherMap format.
        metric: One of 'temperature', 'humidity', 'wind_speed'.
        operator: One of 'gt', 'lt', 'gte', 'lte'.
        value: The threshold value to compare against.

    Returns:
        True if the threshold condition is met, False otherwise.
    """
    # Extract metric value from weather data
    metric_extractors: dict = {
        "temperature": lambda d: d["main"]["temp"],
        "humidity": lambda d: d["main"]["humidity"],
        "wind_speed": lambda d: d["wind"]["speed"],
    }

    if metric not in metric_extractors:
        raise ValueError(f"Unknown metric: {metric!r}. Must be one of {list(metric_extractors)}")

    actual_value: float = metric_extractors[metric](weather_data)

    # Evaluate operator
    operators: dict = {
        "gt": lambda a, b: a > b,
        "lt": lambda a, b: a < b,
        "gte": lambda a, b: a >= b,
        "lte": lambda a, b: a <= b,
    }

    if operator not in operators:
        raise ValueError(f"Unknown operator: {operator!r}. Must be one of {list(operators)}")

    return operators[operator](actual_value, value)


def evaluate_city_thresholds(
    city_id: int,
    weather_data: dict,
    conn: sqlite3.Connection | None = None,
) -> list[dict]:
    """Evaluate all enabled thresholds for a city and log any alerts.

    Args:
        city_id: The city's database ID.
        weather_data: Current weather data for the city.
        conn: Optional database connection (uses get_connection() if not provided).

    Returns:
        List of alert dicts that were triggered.
    """
    if conn is None:
        conn = get_connection()
        if conn is None:
            raise RuntimeError("No database connection available")

    # Fetch enabled thresholds for this city
    cursor = conn.execute(
        "SELECT id, metric, operator, value FROM thresholds WHERE city_id = ? AND enabled = 1",
        (city_id,),
    )
    thresholds = cursor.fetchall()

    triggered_alerts: list[dict] = []
    now = datetime.now(timezone.utc).isoformat()

    for threshold in thresholds:
        threshold_id = threshold["id"]
        metric = threshold["metric"]
        operator = threshold["operator"]
        threshold_value = threshold["value"]

        try:
            exceeded = check_threshold(weather_data, metric, operator, threshold_value)
        except (KeyError, ValueError):
            continue

        if exceeded:
            # Extract actual metric value for logging
            metric_value: float
            if metric == "temperature":
                metric_value = weather_data["main"]["temp"]
            elif metric == "humidity":
                metric_value = weather_data["main"]["humidity"]
            else:  # wind_speed
                metric_value = weather_data["wind"]["speed"]

            message = (
                f"Alert: {metric} is {metric_value} "
                f"({operator} {threshold_value})"
            )

            conn.execute(
                """
                INSERT INTO alert_log (city_id, threshold_id, triggered_at, metric_value, message)
                VALUES (?, ?, ?, ?, ?)
                """,
                (city_id, threshold_id, now, metric_value, message),
            )
            conn.commit()

            triggered_alerts.append({
                "city_id": city_id,
                "threshold_id": threshold_id,
                "triggered_at": now,
                "metric_value": metric_value,
                "message": message,
            })

    return triggered_alerts
