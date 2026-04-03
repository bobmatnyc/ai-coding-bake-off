"""Tests for board management endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestBoardCreate:
    """Test board creation."""

    def test_create_board(self, client: TestClient, auth_headers: dict) -> None:
        """Should create a board with default columns."""
        resp = client.post(
            "/api/boards",
            json={"name": "My Board", "description": "Test description"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "My Board"
        assert "id" in data

    def test_create_board_creates_default_columns(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Creating a board should create 3 default columns."""
        board_resp = client.post(
            "/api/boards",
            json={"name": "Kanban Board"},
            headers=auth_headers,
        )
        board_id = board_resp.json()["id"]

        detail_resp = client.get(f"/api/boards/{board_id}", headers=auth_headers)
        assert detail_resp.status_code == 200
        data = detail_resp.json()
        assert len(data["columns"]) == 3
        col_names = [c["name"] for c in data["columns"]]
        assert "To Do" in col_names
        assert "In Progress" in col_names
        assert "Done" in col_names

    def test_create_board_requires_auth(self, client: TestClient) -> None:
        """Should require authentication to create board."""
        resp = client.post("/api/boards", json={"name": "Unauth Board"})
        assert resp.status_code in (401, 403)

    def test_create_board_missing_name(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Should reject board without name."""
        resp = client.post("/api/boards", json={}, headers=auth_headers)
        assert resp.status_code == 422


class TestBoardList:
    """Test board listing."""

    def test_list_boards(self, client: TestClient, auth_headers: dict) -> None:
        """Should list all boards."""
        client.post("/api/boards", json={"name": "Board A"}, headers=auth_headers)
        client.post("/api/boards", json={"name": "Board B"}, headers=auth_headers)

        resp = client.get("/api/boards", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_list_boards_requires_auth(self, client: TestClient) -> None:
        """Should require authentication."""
        resp = client.get("/api/boards")
        assert resp.status_code in (401, 403)


class TestBoardGet:
    """Test getting a single board."""

    def test_get_board(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Should return board with columns and tasks."""
        resp = client.get(f"/api/boards/{sample_board['id']}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == sample_board["id"]
        assert data["name"] == sample_board["name"]
        assert "columns" in data

    def test_get_nonexistent_board(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Should return 404 for non-existent board."""
        resp = client.get("/api/boards/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestBoardUpdate:
    """Test board updates."""

    def test_update_board(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Should update board name and description."""
        resp = client.put(
            f"/api/boards/{sample_board['id']}",
            json={"name": "Updated Board", "description": "New description"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Updated Board"

    def test_update_nonexistent_board(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Should return 404 for non-existent board."""
        resp = client.put(
            "/api/boards/99999",
            json={"name": "Ghost Board"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


class TestBoardDelete:
    """Test board deletion."""

    def test_delete_board_requires_admin(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Regular users cannot delete boards."""
        resp = client.delete(
            f"/api/boards/{sample_board['id']}",
            headers=auth_headers,
        )
        assert resp.status_code == 403

    def test_delete_board_as_admin(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        """Admin can delete boards."""
        board_resp = client.post(
            "/api/boards",
            json={"name": "Delete Me"},
            headers=admin_headers,
        )
        board_id = board_resp.json()["id"]

        resp = client.delete(f"/api/boards/{board_id}", headers=admin_headers)
        assert resp.status_code == 204

        # Verify deleted
        get_resp = client.get(f"/api/boards/{board_id}", headers=admin_headers)
        assert get_resp.status_code == 404


class TestColumnManagement:
    """Test column management on boards."""

    def test_add_column_to_board(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Should add a column to a board."""
        resp = client.post(
            f"/api/boards/{sample_board['id']}/columns",
            json={"name": "Review", "position": 3},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Review"
        assert data["board_id"] == sample_board["id"]

    def test_update_column(
        self, client: TestClient, auth_headers: dict, sample_column: dict
    ) -> None:
        """Should update a column name."""
        resp = client.put(
            f"/api/columns/{sample_column['id']}",
            json={"name": "Backlog"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Backlog"

    def test_delete_column(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Should delete a column."""
        # Add a column to delete
        col_resp = client.post(
            f"/api/boards/{sample_board['id']}/columns",
            json={"name": "Temp Column", "position": 10},
            headers=auth_headers,
        )
        col_id = col_resp.json()["id"]

        resp = client.delete(f"/api/columns/{col_id}", headers=auth_headers)
        assert resp.status_code == 204


class TestBoardActivity:
    """Test board activity feed."""

    def test_board_activity_endpoint(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Should return activity list for a board."""
        resp = client.get(
            f"/api/boards/{sample_board['id']}/activity",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_board_creation_logs_activity(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Creating a board should log an activity entry."""
        board_resp = client.post(
            "/api/boards",
            json={"name": "Activity Test Board"},
            headers=auth_headers,
        )
        board_id = board_resp.json()["id"]

        activity_resp = client.get(
            f"/api/boards/{board_id}/activity",
            headers=auth_headers,
        )
        activities = activity_resp.json()
        assert len(activities) >= 1
        actions = [a["action"] for a in activities]
        assert "created" in actions
