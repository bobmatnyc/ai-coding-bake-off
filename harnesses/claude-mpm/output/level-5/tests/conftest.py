"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from task_board.models import Base
from task_board.database import get_db
from task_board.app import app


@pytest.fixture(scope="function")
def db_engine():
    """Create a fresh in-memory database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a database session for testing."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_engine):
    """Create a test client with a fresh database."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def registered_user(client):
    """Register and return a test user."""
    resp = client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "password": "TestPass123!",
            "display_name": "Test User",
        },
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture(scope="function")
def auth_token(client, registered_user):
    """Login and return a JWT token."""
    resp = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "TestPass123!"},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.fixture(scope="function")
def auth_headers(auth_token):
    """Return Authorization headers."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="function")
def admin_user(client):
    """Register an admin user directly in DB."""
    from task_board.models import User, Role
    from task_board.auth import hash_password
    # We need to access the db through the override
    resp = client.post(
        "/api/auth/register",
        json={
            "email": "admin@example.com",
            "password": "AdminPass123!",
            "display_name": "Admin User",
        },
    )
    user_id = resp.json()["id"]
    # Promote to admin via direct DB manipulation isn't straightforward here
    # Instead, log in as this user (will be member), then update role in DB
    return resp.json()


@pytest.fixture(scope="function")
def admin_token(client, db_session):
    """Create admin user and return token."""
    from task_board.models import User, Role
    from task_board.auth import hash_password

    # Register admin
    resp = client.post(
        "/api/auth/register",
        json={
            "email": "admin@example.com",
            "password": "AdminPass123!",
            "display_name": "Admin User",
        },
    )
    user_id = resp.json()["id"]

    # Promote to admin in DB
    user = db_session.get(User, user_id)
    if user:
        user.role = Role.admin
        db_session.commit()

    # Login
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "AdminPass123!"},
    )
    return login_resp.json()["access_token"]


@pytest.fixture(scope="function")
def admin_headers(admin_token):
    """Return admin Authorization headers."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="function")
def sample_board(client, auth_headers):
    """Create and return a sample board."""
    resp = client.post(
        "/api/boards",
        json={"name": "Sample Board", "description": "A sample board for testing"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture(scope="function")
def sample_column(client, auth_headers, sample_board):
    """Return the first column of the sample board."""
    board_resp = client.get(f"/api/boards/{sample_board['id']}", headers=auth_headers)
    board_data = board_resp.json()
    columns = board_data.get("columns", [])
    assert len(columns) > 0, "Board should have default columns"
    return columns[0]


@pytest.fixture(scope="function")
def sample_task(client, auth_headers, sample_column):
    """Create and return a sample task."""
    resp = client.post(
        "/api/tasks",
        json={
            "title": "Sample Task",
            "description": "A sample task for testing",
            "column_id": sample_column["id"],
            "priority": "medium",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    return resp.json()
