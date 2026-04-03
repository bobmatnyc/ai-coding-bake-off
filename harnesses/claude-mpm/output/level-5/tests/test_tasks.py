"""Tests for task management endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestTaskCreate:
    """Test task creation."""

    def test_create_task(
        self,
        client: TestClient,
        auth_headers: dict,
        sample_column: dict,
    ) -> None:
        """Should create a task in a column."""
        resp = client.post(
            "/api/tasks",
            json={
                "title": "New Task",
                "description": "Task description",
                "column_id": sample_column["id"],
                "priority": "high",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "New Task"
        assert data["column_id"] == sample_column["id"]
        assert data["priority"] == "high"
        assert "id" in data

    def test_create_task_invalid_column(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Should return 404 for non-existent column."""
        resp = client.post(
            "/api/tasks",
            json={"title": "Task", "column_id": 99999},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_create_task_invalid_priority(
        self, client: TestClient, auth_headers: dict, sample_column: dict
    ) -> None:
        """Should reject invalid priority value."""
        resp = client.post(
            "/api/tasks",
            json={
                "title": "Task",
                "column_id": sample_column["id"],
                "priority": "invalid_priority",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 400

    def test_create_task_missing_title(
        self, client: TestClient, auth_headers: dict, sample_column: dict
    ) -> None:
        """Should reject task without title."""
        resp = client.post(
            "/api/tasks",
            json={"column_id": sample_column["id"]},
            headers=auth_headers,
        )
        assert resp.status_code == 422

    def test_create_task_requires_auth(
        self, client: TestClient, sample_column: dict
    ) -> None:
        """Should require authentication."""
        resp = client.post(
            "/api/tasks",
            json={"title": "Unauth Task", "column_id": sample_column["id"]},
        )
        assert resp.status_code in (401, 403)


class TestTaskList:
    """Test task listing."""

    def test_list_tasks(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Should list all tasks."""
        resp = client.get("/api/tasks", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_tasks_filter_by_column(
        self, client: TestClient, auth_headers: dict, sample_task: dict, sample_column: dict
    ) -> None:
        """Should filter tasks by column_id."""
        resp = client.get(
            f"/api/tasks?column_id={sample_column['id']}",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert all(t["column_id"] == sample_column["id"] for t in data)

    def test_list_tasks_filter_by_board(
        self, client: TestClient, auth_headers: dict, sample_task: dict, sample_board: dict
    ) -> None:
        """Should filter tasks by board_id."""
        resp = client.get(
            f"/api/tasks?board_id={sample_board['id']}",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestTaskGet:
    """Test getting a single task."""

    def test_get_task(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Should return a single task by ID."""
        resp = client.get(f"/api/tasks/{sample_task['id']}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == sample_task["id"]
        assert data["title"] == sample_task["title"]

    def test_get_nonexistent_task(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Should return 404 for non-existent task."""
        resp = client.get("/api/tasks/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestTaskUpdate:
    """Test task updates."""

    def test_update_task_title(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Should update task title."""
        resp = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": "Updated Title"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated Title"

    def test_update_task_priority(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Should update task priority."""
        resp = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"priority": "low"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["priority"] == "low"

    def test_update_task_invalid_priority(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Should reject invalid priority."""
        resp = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"priority": "urgent"},
            headers=auth_headers,
        )
        assert resp.status_code == 400

    def test_update_nonexistent_task(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Should return 404."""
        resp = client.put(
            "/api/tasks/99999",
            json={"title": "Ghost Task"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


class TestTaskDelete:
    """Test task deletion."""

    def test_delete_task_requires_admin(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Regular users cannot delete tasks."""
        resp = client.delete(
            f"/api/tasks/{sample_task['id']}",
            headers=auth_headers,
        )
        assert resp.status_code == 403

    def test_delete_task_as_admin(
        self,
        client: TestClient,
        admin_headers: dict,
        sample_column: dict,
    ) -> None:
        """Admin can delete tasks."""
        task_resp = client.post(
            "/api/tasks",
            json={"title": "Delete Me", "column_id": sample_column["id"]},
            headers=admin_headers,
        )
        task_id = task_resp.json()["id"]

        resp = client.delete(f"/api/tasks/{task_id}", headers=admin_headers)
        assert resp.status_code == 204

        # Verify deleted
        get_resp = client.get(f"/api/tasks/{task_id}", headers=admin_headers)
        assert get_resp.status_code == 404


class TestTaskMove:
    """Test task movement between columns."""

    def test_move_task_to_different_column(
        self,
        client: TestClient,
        auth_headers: dict,
        sample_task: dict,
        sample_board: dict,
    ) -> None:
        """Should move a task to a different column."""
        # Get all columns
        board_resp = client.get(f"/api/boards/{sample_board['id']}", headers=auth_headers)
        columns = board_resp.json()["columns"]
        assert len(columns) >= 2

        # Move to the second column
        target_col = columns[1]

        resp = client.patch(
            f"/api/tasks/{sample_task['id']}/move",
            json={"column_id": target_col["id"]},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["column_id"] == target_col["id"]

    def test_move_task_invalid_column(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ) -> None:
        """Should return 404 when target column doesn't exist."""
        resp = client.patch(
            f"/api/tasks/{sample_task['id']}/move",
            json={"column_id": 99999},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_move_nonexistent_task(
        self, client: TestClient, auth_headers: dict, sample_column: dict
    ) -> None:
        """Should return 404 for non-existent task."""
        resp = client.patch(
            "/api/tasks/99999/move",
            json={"column_id": sample_column["id"]},
            headers=auth_headers,
        )
        assert resp.status_code == 404
