"""Provided test suite for Level 3: Weather Alerting Service.

Tests use mock weather data and an in-memory database.
Agents must pass these tests and should write additional ones.
"""

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_weather_data() -> dict:
    """Load mock weather API response."""
    with open(FIXTURES_DIR / "mock_weather_response.json") as f:
        return json.load(f)


@pytest.fixture
def app_client():
    """Create a test client for the weather alerter API.

    Agents may use FastAPI TestClient or Flask test_client.
    This fixture tries both common patterns.
    """
    try:
        # FastAPI pattern
        from fastapi.testclient import TestClient
        try:
            from weather_alerter.app import app
        except ImportError:
            from app import app
        client = TestClient(app)
        return client
    except ImportError:
        pass

    try:
        # Flask pattern
        try:
            from weather_alerter.app import create_app
        except ImportError:
            from app import create_app
        app = create_app(testing=True)
        return app.test_client()
    except (ImportError, TypeError):
        pass

    pytest.skip("Could not create test client. Ensure app is importable.")


class TestHealthCheck:
    """Test the health check endpoint."""

    def test_health_returns_200(self, app_client) -> None:
        """Health endpoint should return 200."""
        response = app_client.get("/api/health")
        assert response.status_code == 200


class TestCityCRUD:
    """Test city management endpoints."""

    def test_create_city(self, app_client) -> None:
        """Should create a new city."""
        response = app_client.post(
            "/api/cities",
            json={
                "name": "San Francisco",
                "latitude": 37.7749,
                "longitude": -122.4194,
            },
        )
        assert response.status_code in (200, 201)

        data = response.json() if hasattr(response, 'json') and callable(response.json) else json.loads(response.data)
        assert data["name"] == "San Francisco"
        assert "id" in data

    def test_list_cities(self, app_client) -> None:
        """Should list all cities."""
        # Create a city first
        app_client.post(
            "/api/cities",
            json={"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503},
        )

        response = app_client.get("/api/cities")
        assert response.status_code == 200

        data = response.json() if hasattr(response, 'json') and callable(response.json) else json.loads(response.data)

        # Support both list response and wrapped response
        cities = data if isinstance(data, list) else data.get("cities", data.get("data", []))
        assert len(cities) >= 1

    def test_delete_city(self, app_client) -> None:
        """Should delete a city."""
        # Create then delete
        create_resp = app_client.post(
            "/api/cities",
            json={"name": "Delete Me", "latitude": 0.0, "longitude": 0.0},
        )
        create_data = create_resp.json() if hasattr(create_resp, 'json') and callable(create_resp.json) else json.loads(create_resp.data)
        city_id = create_data["id"]

        delete_resp = app_client.delete(f"/api/cities/{city_id}")
        assert delete_resp.status_code in (200, 204)


class TestThresholds:
    """Test alert threshold management."""

    def test_create_threshold(self, app_client) -> None:
        """Should create an alert threshold for a city."""
        # Create city first
        city_resp = app_client.post(
            "/api/cities",
            json={"name": "Threshold City", "latitude": 0.0, "longitude": 0.0},
        )
        city_data = city_resp.json() if hasattr(city_resp, 'json') and callable(city_resp.json) else json.loads(city_resp.data)
        city_id = city_data["id"]

        # Create threshold
        threshold_resp = app_client.post(
            f"/api/cities/{city_id}/thresholds",
            json={"metric": "temperature", "operator": "gt", "value": 35.0},
        )
        assert threshold_resp.status_code in (200, 201)

        threshold_data = threshold_resp.json() if hasattr(threshold_resp, 'json') and callable(threshold_resp.json) else json.loads(threshold_resp.data)
        assert threshold_data["metric"] == "temperature"
        assert threshold_data["operator"] == "gt"
        assert threshold_data["value"] == 35.0


class TestAlertLogic:
    """Test the core alert evaluation logic."""

    def test_threshold_exceeded_triggers_alert(self, mock_weather_data) -> None:
        """When a metric exceeds the threshold, an alert should be triggered."""
        # Import alert checking logic
        try:
            from weather_alerter.alerts import check_threshold
        except ImportError:
            try:
                from alerts import check_threshold
            except ImportError:
                pytest.skip("Could not import check_threshold function")

        # Temperature in mock data is 22.5
        # Threshold: temperature > 20 should trigger
        result = check_threshold(
            weather_data=mock_weather_data,
            metric="temperature",
            operator="gt",
            value=20.0,
        )
        assert result is True, "Threshold temperature > 20 should be triggered (actual: 22.5)"

    def test_threshold_not_exceeded_no_alert(self, mock_weather_data) -> None:
        """When a metric is within threshold, no alert should be triggered."""
        try:
            from weather_alerter.alerts import check_threshold
        except ImportError:
            try:
                from alerts import check_threshold
            except ImportError:
                pytest.skip("Could not import check_threshold function")

        # Temperature in mock data is 22.5
        # Threshold: temperature > 30 should NOT trigger
        result = check_threshold(
            weather_data=mock_weather_data,
            metric="temperature",
            operator="gt",
            value=30.0,
        )
        assert result is False, "Threshold temperature > 30 should NOT be triggered (actual: 22.5)"
