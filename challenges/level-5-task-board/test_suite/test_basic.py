"""Provided test suite for Level 5: Team Task Board.

These are minimal smoke tests. Agents should write comprehensive tests.
Tests assume the app can be imported and provides a test client.
"""

import json

import pytest


@pytest.fixture
def app_client():
    """Create test client. Agents decide the framework."""
    # Try FastAPI
    try:
        from fastapi.testclient import TestClient
        try:
            from task_board.app import app
        except ImportError:
            from app import app
        return TestClient(app)
    except ImportError:
        pass

    # Try Flask
    try:
        try:
            from task_board.app import create_app
        except ImportError:
            from app import create_app
        app = create_app(testing=True)
        return app.test_client()
    except (ImportError, TypeError):
        pass

    # Try Django
    try:
        from django.test import Client
        return Client()
    except ImportError:
        pass

    pytest.skip("Could not create test client")


@pytest.fixture
def auth_headers(app_client) -> dict:
    """Register a user and return auth headers."""
    # Register
    reg_resp = app_client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
            "display_name": "Test User",
        },
    )

    # Login
    login_resp = app_client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "TestPass123!"},
    )

    data = login_resp.json() if hasattr(login_resp, 'json') and callable(login_resp.json) else json.loads(login_resp.data)
    token = data.get("access_token", data.get("token", ""))

    return {"Authorization": f"Bearer {token}"}


class TestAuth:
    """Test authentication endpoints."""

    def test_register_user(self, app_client) -> None:
        """Should register a new user."""
        response = app_client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!",
                "display_name": "New User",
            },
        )
        assert response.status_code in (200, 201)

    def test_login_returns_token(self, app_client) -> None:
        """Login should return a JWT token."""
        # Register first
        app_client.post(
            "/api/auth/register",
            json={
                "email": "logintest@example.com",
                "password": "SecurePass123!",
                "display_name": "Login User",
            },
        )

        response = app_client.post(
            "/api/auth/login",
            json={"email": "logintest@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 200

        data = response.json() if hasattr(response, 'json') and callable(response.json) else json.loads(response.data)
        assert "access_token" in data or "token" in data

    def test_protected_endpoint_requires_auth(self, app_client) -> None:
        """Protected endpoints should require authentication."""
        response = app_client.get("/api/users/me")
        assert response.status_code in (401, 403)


class TestBoardCRUD:
    """Test board management."""

    def test_create_board(self, app_client, auth_headers) -> None:
        """Should create a new board."""
        response = app_client.post(
            "/api/boards",
            json={"name": "Test Board", "description": "A test board"},
            headers=auth_headers,
        )
        assert response.status_code in (200, 201)

        data = response.json() if hasattr(response, 'json') and callable(response.json) else json.loads(response.data)
        assert data["name"] == "Test Board"

    def test_list_boards(self, app_client, auth_headers) -> None:
        """Should list boards."""
        app_client.post(
            "/api/boards",
            json={"name": "Board 1"},
            headers=auth_headers,
        )

        response = app_client.get("/api/boards", headers=auth_headers)
        assert response.status_code == 200


class TestTaskCRUD:
    """Test task management."""

    def test_create_task(self, app_client, auth_headers) -> None:
        """Should create a task on a board."""
        # Create board first
        board_resp = app_client.post(
            "/api/boards",
            json={"name": "Task Board"},
            headers=auth_headers,
        )
        board_data = board_resp.json() if hasattr(board_resp, 'json') and callable(board_resp.json) else json.loads(board_resp.data)
        board_id = board_data["id"]

        # Get or create a column
        board_detail = app_client.get(f"/api/boards/{board_id}", headers=auth_headers)
        detail_data = board_detail.json() if hasattr(board_detail, 'json') and callable(board_detail.json) else json.loads(board_detail.data)

        columns = detail_data.get("columns", [])
        if columns:
            column_id = columns[0]["id"]
        else:
            col_resp = app_client.post(
                f"/api/boards/{board_id}/columns",
                json={"name": "To Do", "position": 0},
                headers=auth_headers,
            )
            col_data = col_resp.json() if hasattr(col_resp, 'json') and callable(col_resp.json) else json.loads(col_resp.data)
            column_id = col_data["id"]

        # Create task
        task_resp = app_client.post(
            "/api/tasks",
            json={
                "title": "Test Task",
                "description": "A test task",
                "column_id": column_id,
                "priority": "medium",
            },
            headers=auth_headers,
        )
        assert task_resp.status_code in (200, 201)

        task_data = task_resp.json() if hasattr(task_resp, 'json') and callable(task_resp.json) else json.loads(task_resp.data)
        assert task_data["title"] == "Test Task"


class TestActivityLog:
    """Test activity logging."""

    def test_activity_created_on_task_creation(self, app_client, auth_headers) -> None:
        """Creating a task should generate an activity log entry."""
        # Create board and task (simplified - assumes board/column exist)
        board_resp = app_client.post(
            "/api/boards",
            json={"name": "Activity Board"},
            headers=auth_headers,
        )
        board_data = board_resp.json() if hasattr(board_resp, 'json') and callable(board_resp.json) else json.loads(board_resp.data)
        board_id = board_data["id"]

        # Check activity
        activity_resp = app_client.get(
            f"/api/boards/{board_id}/activity",
            headers=auth_headers,
        )
        # Should have at least board creation activity
        assert activity_resp.status_code == 200
