import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from auth.app import models
from auth.app.main import app
from common.database import Base, get_db

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_create_user():
    """Test user creation endpoint."""
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword", "roles": []},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_create_user_duplicate_email():
    """Test that creating a user with duplicate email fails."""
    # Create first user
    client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword",
            "roles": [],
        },
    )

    # Try to create second user with same email
    response = client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword2",
            "roles": [],
        },
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_create_role():
    """Test role creation endpoint."""
    response = client.post(
        "/roles/",
        json={"name": "veterinario", "description": "Veterinario del sistema"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "veterinario"
    assert data["description"] == "Veterinario del sistema"


def test_login():
    """Test login functionality."""
    # First create a user
    client.post(
        "/users/",
        json={"email": "login@example.com", "password": "loginpassword", "roles": []},
    )

    # Try to login
    response = client.post(
        "/token", data={"username": "login@example.com", "password": "loginpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/token",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Auth Service"
