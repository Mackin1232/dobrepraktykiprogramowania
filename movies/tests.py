import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

admin = {
    "username": "admin",
    "password": "admin123"
}

olduser = {
    "username": "Mackin",
    "password": "123"
}

newuser = {
    "username": "testuser",
    "password": "test"
}

fail = {
    "username": "fail",
    "password": "fail123"
}


class TestClass:

    def test_login_success(self):
        response = client.post("/login", json=admin)
        assert "access_token" in response.json().keys()

    def test_login_failure(self):
        response = client.post("/login", json=fail)
        assert response.json()['detail'] == "Invalid credentials"

    def test_adduser_success(self):
        token = client.post("/login", json=admin).json()['access_token']
        add_response = client.post("/users", json=newuser, headers={"Authorization": f"Bearer {token}"})

        login_response = client.post("/login", json=newuser)
        assert "access_token" in login_response.json().keys()

    def test_adduser_fail(self):
        token = client.post("/login", json=olduser).json()['access_token']
        add_response = client.post("/users", json=fail, headers={"Authorization": f"Bearer {token}"})
        assert add_response.json()['detail'] == "Access denied"

    def test_userdetails_success(self):
        token = client.post("/login", json=olduser).json()['access_token']
        details_response = client.get("/user_details", headers={"Authorization": f"Bearer {token}"}).json()
        assert details_response['username'] == olduser['username'] and details_response['role'] == "ROLE_USER"

    def test_userdetails_fail(self):
        token = client.post("/login", json=olduser).json()['access_token'] + "a"
        details_response = client.get("/user_details", headers={"Authorization": f"Bearer {token}"})
        assert details_response.json()['detail'] == "Invalid token"


pytest.main()
