"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestRegister:
    """Test user registration."""

    def test_register_new_user(self, client: TestClient) -> None:
        """Should register a new user successfully."""
        resp = client.post(
            "/api/auth/register",
            json={
                "email": "new@example.com",
                "password": "Password123!",
                "display_name": "New User",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "new@example.com"
        assert data["display_name"] == "New User"
        assert "id" in data
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_duplicate_email(self, client: TestClient) -> None:
        """Should reject duplicate email registration."""
        payload = {
            "email": "dup@example.com",
            "password": "Password123!",
            "display_name": "User",
        }
        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 400

    def test_register_missing_fields(self, client: TestClient) -> None:
        """Should reject incomplete registration."""
        resp = client.post(
            "/api/auth/register",
            json={"email": "incomplete@example.com"},
        )
        assert resp.status_code == 422


class TestLogin:
    """Test user login."""

    def test_login_success(self, client: TestClient) -> None:
        """Should return access token on valid login."""
        client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "Password123!",
                "display_name": "Login User",
            },
        )
        resp = client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "Password123!"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 10

    def test_login_wrong_password(self, client: TestClient) -> None:
        """Should reject wrong password."""
        client.post(
            "/api/auth/register",
            json={
                "email": "pwtest@example.com",
                "password": "Password123!",
                "display_name": "User",
            },
        )
        resp = client.post(
            "/api/auth/login",
            json={"email": "pwtest@example.com", "password": "WrongPass!"},
        )
        assert resp.status_code == 401

    def test_login_unknown_email(self, client: TestClient) -> None:
        """Should reject unknown email."""
        resp = client.post(
            "/api/auth/login",
            json={"email": "ghost@example.com", "password": "Password123!"},
        )
        assert resp.status_code == 401

    def test_protected_endpoint_without_token(self, client: TestClient) -> None:
        """Should reject requests without auth token."""
        resp = client.get("/api/users/me")
        assert resp.status_code in (401, 403)

    def test_protected_endpoint_with_invalid_token(self, client: TestClient) -> None:
        """Should reject invalid auth tokens."""
        resp = client.get(
            "/api/users/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert resp.status_code in (401, 403)

    def test_me_endpoint_returns_user(self, client: TestClient, auth_headers: dict) -> None:
        """Authenticated /me should return user data."""
        resp = client.get("/api/users/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "id" in data
        assert "email" in data
        assert "display_name" in data
        assert data["email"] == "user@example.com"
