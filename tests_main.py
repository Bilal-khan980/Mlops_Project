import pytest
import httpx

BASE_URL = "http://0.0.0.0:8000"

def test_signup():
    response = httpx.post(f"{BASE_URL}/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_signup_existing_username():
    httpx.post(f"{BASE_URL}/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    response = httpx.post(f"{BASE_URL}/signup", json={
        "username": "testuser",
        "email": "newemail@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

def test_login_success():
    httpx.post(f"{BASE_URL}/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    response = httpx.post(f"{BASE_URL}/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_predict_success():
    # Mock the model.pkl or ensure it works as expected
    response = httpx.post(f"{BASE_URL}/predict", json={
        "humidity": 70,
        "wind_speed": 10
    })
    assert response.status_code == 200
    assert "temperature" in response.json()
