import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def unique_email():
    return f"test-{uuid.uuid4()}@example.com"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register(client):
    email = unique_email()
    response = client.post("/register", json={
        "email": email,
        "username": f"user-{uuid.uuid4()}",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == email

def test_register_duplicate(client):
    email = unique_email()
    username = f"user-{uuid.uuid4()}"
    
    client.post("/register", json={
        "email": email,
        "username": username,
        "password": "pass1"
    })
    
    response = client.post("/register", json={
        "email": email,
        "username": f"other-{uuid.uuid4()}",
        "password": "pass2"
    })
    assert response.status_code == 400

def test_login(client):
    email = unique_email()
    username = f"user-{uuid.uuid4()}"
    
    client.post("/register", json={
        "email": email,
        "username": username,
        "password": "pass123"
    })
    
    response = client.post("/login", json={
        "email": email,
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client):
    response = client.post("/login", json={
        "email": f"nonexistent-{uuid.uuid4()}@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
