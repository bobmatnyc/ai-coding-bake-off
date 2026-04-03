"""Pydantic request/response models for the weather alerter API."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


# --- City Models ---

class CityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    enabled: bool = True


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    enabled: Optional[bool] = None


class CityResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    enabled: bool
    created_at: str


# --- Threshold Models ---

MetricType = Literal["temperature", "humidity", "wind_speed"]
OperatorType = Literal["gt", "lt", "gte", "lte"]


class ThresholdCreate(BaseModel):
    metric: MetricType
    operator: OperatorType
    value: float
    enabled: bool = True


class ThresholdResponse(BaseModel):
    id: int
    city_id: int
    metric: str
    operator: str
    value: float
    enabled: bool


# --- Alert Models ---

class AlertResponse(BaseModel):
    id: int
    city_id: int
    threshold_id: int
    triggered_at: str
    metric_value: float
    message: str


# --- Weather Models ---

class WeatherMain(BaseModel):
    temp: float
    feels_like: float
    humidity: int
    pressure: int


class WeatherWind(BaseModel):
    speed: float
    deg: Optional[int] = None


class WeatherCondition(BaseModel):
    main: str
    description: str


class WeatherResponse(BaseModel):
    city_id: int
    city_name: str
    main: WeatherMain
    wind: WeatherWind
    weather: list[WeatherCondition]
    name: str


# --- Health Model ---

class HealthResponse(BaseModel):
    status: str
