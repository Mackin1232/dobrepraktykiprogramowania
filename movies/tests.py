import pytest
from jwt import decode
from fastapi.testclient import TestClient
from auth.login_token import verify_token
from auth.create_token import SECRET_KEY, ALGORITHM
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

newMovie = {
    "title": "Rush (2013)",
    "genres": "Biography|Drama|Sport"
}


class TestClass:

    def test_login_success(self):
        response = client.post("/login", json=admin).json()
        assert "access_token" in response.keys()
        payload = decode(response['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        assert username == admin["username"]
        assert role == "ROLE_ADMIN"

    def test_login_failure(self):
        response = client.post("/login", json=fail)
        assert response.json()['detail'] == "Invalid credentials"

    def test_adduser_success(self):
        token = client.post("/login", json=admin).json()['access_token']
        add_response = client.post("/users", json=newuser, headers={"Authorization": f"Bearer {token}"})

        login_response = client.post("/login", json=newuser).json()
        assert "access_token" in login_response.keys()
        payload = decode(login_response['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        assert username == newuser["username"]
        assert role == "ROLE_USER"

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

    def test_addmovie_success(self):
        token = client.post("/login", json=admin).json()['access_token']
        add_response = client.post("/movies", json=newMovie,headers={"Authorization": f"Bearer {token}"})
        assert add_response.json()['detail'] == "Added movie Rush (2013)"

pytest.main()
