import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def unique_email():
    """Generate unique email for each test"""
    return f"test-{uuid.uuid4()}@example.com"

def test_health():
    """Health check should return ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register():
    """Registration should create a new user"""
    email = unique_email()
    response = client.post("/register", json={
        "email": email,
        "username": f"user-{uuid.uuid4()}",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == email

def test_register_duplicate():
    """Registration with duplicate email should fail"""
    email = unique_email()
    username = f"user-{uuid.uuid4()}"
    
    # First registration
    client.post("/register", json={
        "email": email,
        "username": username,
        "password": "pass1"
    })
    
    # Second registration with same email
    response = client.post("/register", json={
        "email": email,
        "username": f"other-{uuid.uuid4()}",
        "password": "pass2"
    })
    assert response.status_code == 400

def test_login():
    """Login should return JWT token"""
    email = unique_email()
    username = f"user-{uuid.uuid4()}"
    
    # Register first
    client.post("/register", json={
        "email": email,
        "username": username,
        "password": "pass123"
    })
    
    # Login
    response = client.post("/login", json={
        "email": email,
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid():
    """Login with wrong password should fail"""
    response = client.post("/login", json={
        "email": f"nonexistent-{uuid.uuid4()}@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_get_tasks():
    """Get tasks should return list"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)