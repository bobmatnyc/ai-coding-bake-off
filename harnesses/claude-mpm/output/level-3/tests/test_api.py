"""Comprehensive API tests covering all endpoints."""

import pytest


class TestHealth:
    def test_health_check(self, app_client):
        resp = app_client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestCitiesCreate:
    def test_create_city_returns_201(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
        )
        assert resp.status_code == 201

    def test_create_city_returns_id(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503},
        )
        data = resp.json()
        assert "id" in data
        assert data["id"] > 0

    def test_create_city_stores_fields(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"name": "Paris", "latitude": 48.8566, "longitude": 2.3522},
        )
        data = resp.json()
        assert data["name"] == "Paris"
        assert data["latitude"] == 48.8566
        assert data["longitude"] == 2.3522
        assert data["enabled"] is True
        assert "created_at" in data

    def test_create_city_with_enabled_false(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"name": "Disabled City", "latitude": 0.0, "longitude": 0.0, "enabled": False},
        )
        assert resp.status_code == 201
        assert resp.json()["enabled"] is False

    def test_create_city_invalid_latitude(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"name": "Bad", "latitude": 200.0, "longitude": 0.0},
        )
        assert resp.status_code == 422

    def test_create_city_invalid_longitude(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"name": "Bad", "latitude": 0.0, "longitude": 200.0},
        )
        assert resp.status_code == 422

    def test_create_city_missing_name(self, app_client):
        resp = app_client.post(
            "/api/cities",
            json={"latitude": 0.0, "longitude": 0.0},
        )
        assert resp.status_code == 422


class TestCitiesRead:
    def test_list_cities_empty(self, app_client):
        resp = app_client.get("/api/cities")
        assert resp.status_code == 200
        data = resp.json()
        assert "cities" in data
        assert data["cities"] == []

    def test_list_cities_after_create(self, app_client):
        app_client.post(
            "/api/cities",
            json={"name": "London", "latitude": 51.5, "longitude": -0.1},
        )
        resp = app_client.get("/api/cities")
        assert resp.status_code == 200
        assert len(resp.json()["cities"]) == 1

    def test_get_city_by_id(self, app_client):
        created = app_client.post(
            "/api/cities",
            json={"name": "Berlin", "latitude": 52.5, "longitude": 13.4},
        ).json()
        resp = app_client.get(f"/api/cities/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Berlin"

    def test_get_city_not_found(self, app_client):
        resp = app_client.get("/api/cities/99999")
        assert resp.status_code == 404

    def test_get_city_404_detail(self, app_client):
        resp = app_client.get("/api/cities/99999")
        assert "not found" in resp.json()["detail"].lower()


class TestCitiesUpdate:
    def test_patch_city_name(self, app_client):
        city = app_client.post(
            "/api/cities",
            json={"name": "Old Name", "latitude": 0.0, "longitude": 0.0},
        ).json()
        resp = app_client.patch(
            f"/api/cities/{city['id']}",
            json={"name": "New Name"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

    def test_patch_city_enabled(self, app_client):
        city = app_client.post(
            "/api/cities",
            json={"name": "Test", "latitude": 0.0, "longitude": 0.0},
        ).json()
        resp = app_client.patch(
            f"/api/cities/{city['id']}",
            json={"enabled": False},
        )
        assert resp.status_code == 200
        assert resp.json()["enabled"] is False

    def test_patch_city_not_found(self, app_client):
        resp = app_client.patch("/api/cities/99999", json={"name": "X"})
        assert resp.status_code == 404


class TestCitiesDelete:
    def test_delete_city_returns_204(self, app_client):
        city = app_client.post(
            "/api/cities",
            json={"name": "Delete Me", "latitude": 0.0, "longitude": 0.0},
        ).json()
        resp = app_client.delete(f"/api/cities/{city['id']}")
        assert resp.status_code == 204

    def test_delete_city_removes_from_list(self, app_client):
        city = app_client.post(
            "/api/cities",
            json={"name": "Ephemeral", "latitude": 0.0, "longitude": 0.0},
        ).json()
        app_client.delete(f"/api/cities/{city['id']}")
        resp = app_client.get("/api/cities")
        ids = [c["id"] for c in resp.json()["cities"]]
        assert city["id"] not in ids

    def test_delete_city_not_found(self, app_client):
        resp = app_client.delete("/api/cities/99999")
        assert resp.status_code == 404


class TestThresholds:
    def _make_city(self, client):
        return client.post(
            "/api/cities",
            json={"name": "Threshold City", "latitude": 10.0, "longitude": 10.0},
        ).json()

    def test_create_threshold_returns_201(self, app_client):
        city = self._make_city(app_client)
        resp = app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "temperature", "operator": "gt", "value": 35.0},
        )
        assert resp.status_code == 201

    def test_create_threshold_stores_fields(self, app_client):
        city = self._make_city(app_client)
        resp = app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "humidity", "operator": "lte", "value": 30.0},
        )
        data = resp.json()
        assert data["metric"] == "humidity"
        assert data["operator"] == "lte"
        assert data["value"] == 30.0
        assert data["city_id"] == city["id"]
        assert data["enabled"] is True

    def test_create_threshold_invalid_metric(self, app_client):
        city = self._make_city(app_client)
        resp = app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "pressure", "operator": "gt", "value": 1000.0},
        )
        assert resp.status_code == 422

    def test_create_threshold_invalid_operator(self, app_client):
        city = self._make_city(app_client)
        resp = app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "temperature", "operator": "eq", "value": 20.0},
        )
        assert resp.status_code == 422

    def test_create_threshold_city_not_found(self, app_client):
        resp = app_client.post(
            "/api/cities/99999/thresholds",
            json={"metric": "temperature", "operator": "gt", "value": 35.0},
        )
        assert resp.status_code == 404

    def test_list_thresholds(self, app_client):
        city = self._make_city(app_client)
        app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "temperature", "operator": "gt", "value": 35.0},
        )
        app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "humidity", "operator": "gt", "value": 80.0},
        )
        resp = app_client.get(f"/api/cities/{city['id']}/thresholds")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_list_thresholds_city_not_found(self, app_client):
        resp = app_client.get("/api/cities/99999/thresholds")
        assert resp.status_code == 404

    def test_delete_threshold(self, app_client):
        city = self._make_city(app_client)
        t = app_client.post(
            f"/api/cities/{city['id']}/thresholds",
            json={"metric": "wind_speed", "operator": "gt", "value": 20.0},
        ).json()
        resp = app_client.delete(f"/api/thresholds/{t['id']}")
        assert resp.status_code == 204

    def test_delete_threshold_not_found(self, app_client):
        resp = app_client.delete("/api/thresholds/99999")
        assert resp.status_code == 404

    def test_all_valid_metrics(self, app_client):
        city = self._make_city(app_client)
        for metric in ["temperature", "humidity", "wind_speed"]:
            resp = app_client.post(
                f"/api/cities/{city['id']}/thresholds",
                json={"metric": metric, "operator": "gt", "value": 1.0},
            )
            assert resp.status_code == 201, f"Failed for metric {metric}"

    def test_all_valid_operators(self, app_client):
        city = self._make_city(app_client)
        for operator in ["gt", "lt", "gte", "lte"]:
            resp = app_client.post(
                f"/api/cities/{city['id']}/thresholds",
                json={"metric": "temperature", "operator": operator, "value": 20.0},
            )
            assert resp.status_code == 201, f"Failed for operator {operator}"


class TestAlerts:
    def test_list_alerts_empty(self, app_client):
        resp = app_client.get("/api/alerts")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_alerts_filter_by_city_id(self, app_client):
        resp = app_client.get("/api/alerts?city_id=1")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_alerts_invalid_city_returns_empty(self, app_client):
        resp = app_client.get("/api/alerts?city_id=99999")
        assert resp.status_code == 200
        assert resp.json() == []


class TestWeather:
    def test_weather_city_not_found(self, app_client):
        resp = app_client.get("/api/weather/99999")
        assert resp.status_code == 404

    def test_weather_returns_mock_data(self, app_client):
        city = app_client.post(
            "/api/cities",
            json={"name": "Weather City", "latitude": 40.0, "longitude": -74.0},
        ).json()
        resp = app_client.get(f"/api/weather/{city['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert "main" in data
        assert "wind" in data
        assert data["city_id"] == city["id"]

    def test_weather_mock_temperature(self, app_client):
        city = app_client.post(
            "/api/cities",
            json={"name": "Mock City", "latitude": 0.0, "longitude": 0.0},
        ).json()
        resp = app_client.get(f"/api/weather/{city['id']}")
        data = resp.json()
        assert data["main"]["temp"] == 22.5
        assert data["main"]["humidity"] == 65
        assert data["wind"]["speed"] == 4.12
