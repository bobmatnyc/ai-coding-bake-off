"""Tests for activity logging."""
import pytest
from fastapi.testclient import TestClient


class TestActivityLogging:
    """Test that actions are properly logged as activities."""

    def test_board_creation_creates_activity(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Creating a board should log a 'created' activity."""
        board_resp = client.post(
            "/api/boards",
            json={"name": "Activity Test Board"},
            headers=auth_headers,
        )
        board_id = board_resp.json()["id"]

        resp = client.get(
            f"/api/boards/{board_id}/activity",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        activities = resp.json()
        assert len(activities) >= 1
        assert any(a["action"] == "created" for a in activities)

    def test_task_creation_creates_activity(
        self,
        client: TestClient,
        auth_headers: dict,
        sample_column: dict,
        sample_board: dict,
    ) -> None:
        """Creating a task should log a 'created' activity."""
        task_resp = client.post(
            "/api/tasks",
            json={"title": "Activity Task", "column_id": sample_column["id"]},
            headers=auth_headers,
        )
        assert task_resp.status_code == 201

        resp = client.get(
            f"/api/boards/{sample_board['id']}/activity",
            headers=auth_headers,
        )
        activities = resp.json()
        assert any(
            a["action"] == "created" and a.get("task_id") is not None
            for a in activities
        )

    def test_task_update_creates_activity(
        self,
        client: TestClient,
        auth_headers: dict,
        sample_task: dict,
        sample_board: dict,
    ) -> None:
        """Updating a task should log an 'updated' activity."""
        client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": "Updated Task"},
            headers=auth_headers,
        )

        resp = client.get(
            f"/api/boards/{sample_board['id']}/activity",
            headers=auth_headers,
        )
        activities = resp.json()
        assert any(a["action"] == "updated" for a in activities)

    def test_task_move_creates_activity(
        self,
        client: TestClient,
        auth_headers: dict,
        sample_task: dict,
        sample_board: dict,
    ) -> None:
        """Moving a task should log a 'moved' activity."""
        board_resp = client.get(f"/api/boards/{sample_board['id']}", headers=auth_headers)
        columns = board_resp.json()["columns"]
        target_col = columns[1]  # Move to second column

        client.patch(
            f"/api/tasks/{sample_task['id']}/move",
            json={"column_id": target_col["id"]},
            headers=auth_headers,
        )

        resp = client.get(
            f"/api/boards/{sample_board['id']}/activity",
            headers=auth_headers,
        )
        activities = resp.json()
        assert any(a["action"] == "moved" for a in activities)

    def test_global_activity_endpoint(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Global activity endpoint should return all activities."""
        resp = client.get("/api/activity", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_activity_has_required_fields(
        self, client: TestClient, auth_headers: dict, sample_board: dict
    ) -> None:
        """Activity entries should have required fields."""
        resp = client.get(
            f"/api/boards/{sample_board['id']}/activity",
            headers=auth_headers,
        )
        activities = resp.json()
        assert len(activities) >= 1
        for activity in activities:
            assert "id" in activity
            assert "board_id" in activity
            assert "user_id" in activity
            assert "action" in activity
            assert "created_at" in activity

    def test_activity_ordered_newest_first(
        self,
        client: TestClient,
        auth_headers: dict,
        sample_column: dict,
        sample_board: dict,
    ) -> None:
        """Activities should be ordered newest first."""
        # Create a task to generate activity
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "column_id": sample_column["id"]},
            headers=auth_headers,
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "column_id": sample_column["id"]},
            headers=auth_headers,
        )

        resp = client.get(
            f"/api/boards/{sample_board['id']}/activity",
            headers=auth_headers,
        )
        activities = resp.json()
        if len(activities) >= 2:
            # Newest should be first (created_at descending)
            dates = [a["created_at"] for a in activities if a["created_at"]]
            assert dates == sorted(dates, reverse=True)
