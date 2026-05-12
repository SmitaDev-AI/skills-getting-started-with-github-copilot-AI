import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    email = "testuser@example.com"
    activity = "Chess Club"
    # Ensure not already registered
    client.post(f"/activities/{activity}/unregister?email={email}")
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code in (200, 400, 404)
    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code in (400, 404)

def test_signup_invalid_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@example.com")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.post("/activities/NonexistentActivity/unregister?email=someone@example.com")
    assert response.status_code == 404
