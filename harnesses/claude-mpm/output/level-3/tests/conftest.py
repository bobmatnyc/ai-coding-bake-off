"""Test configuration and fixtures."""

import os
import pytest

os.environ["TESTING"] = "true"
os.environ["WEATHER_MOCK_MODE"] = "true"

from fastapi.testclient import TestClient
from weather_alerter.app import app
from weather_alerter.database import reset_memory_db


@pytest.fixture
def app_client():
    """Provide a test client with a fresh in-memory database per test."""
    reset_memory_db()
    with TestClient(app) as client:
        yield client
