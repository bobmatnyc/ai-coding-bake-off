"""FastAPI application factory for the weather alerter service."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from weather_alerter.database import init_db, reset_memory_db, is_testing
from weather_alerter.routes.alerts import router as alerts_router
from weather_alerter.routes.cities import router as cities_router
from weather_alerter.routes.thresholds import router as thresholds_router
from weather_alerter.routes.weather import router as weather_router
from weather_alerter.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: start/stop DB and scheduler."""
    # Startup
    if is_testing():
        reset_memory_db()
    else:
        init_db()
        start_scheduler()

    yield

    # Shutdown
    if not is_testing():
        stop_scheduler()


app = FastAPI(
    title="Weather Alerter",
    description="A weather monitoring and alerting service.",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(cities_router, prefix="/api")
app.include_router(thresholds_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(weather_router, prefix="/api")


@app.get("/api/health", tags=["health"])
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
