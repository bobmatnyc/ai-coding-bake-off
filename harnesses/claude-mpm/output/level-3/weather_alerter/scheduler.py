"""APScheduler background job for periodic weather checks."""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from weather_alerter.alerts import evaluate_city_thresholds
from weather_alerter.database import get_connection
from weather_alerter.weather_client import get_weather

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def check_all_cities() -> None:
    """Fetch weather for all enabled cities and evaluate thresholds."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT id, name, latitude, longitude FROM cities WHERE enabled = 1"
    )
    cities = cursor.fetchall()

    for city in cities:
        city_id = city["id"]
        city_name = city["name"]
        lat = city["latitude"]
        lon = city["longitude"]

        try:
            weather_data = get_weather(lat, lon)
            alerts = evaluate_city_thresholds(city_id, weather_data, conn)
            if alerts:
                logger.info(
                    "City %s triggered %d alert(s)", city_name, len(alerts)
                )
        except Exception as exc:  # noqa: BLE001
            logger.error("Error checking city %s: %s", city_name, exc)


def get_scheduler() -> BackgroundScheduler:
    """Get or create the global scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
    return _scheduler


def start_scheduler(interval_seconds: int = 300) -> None:
    """Start the background scheduler.

    Args:
        interval_seconds: How often to poll weather data (default: 5 minutes).
    """
    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.add_job(
            check_all_cities,
            "interval",
            seconds=interval_seconds,
            id="weather_check",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("Weather scheduler started (interval=%ds)", interval_seconds)


def stop_scheduler() -> None:
    """Stop the background scheduler."""
    scheduler = get_scheduler()
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Weather scheduler stopped")
