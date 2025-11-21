import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup(client: AsyncClient):
    """Test user signup"""
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "name": "New User"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient, test_user):
    """Test signup with existing email"""
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": test_user.email,
            "password": "password123",
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    """Test user login"""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": test_user.email,
            "password": "testpassword123",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user):
    """Test login with invalid credentials"""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": test_user.email,
            "password": "wrongpassword",
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user, auth_headers):
    """Test getting current user info"""
    response = await client.get(
        "/api/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, test_user, auth_headers):
    """Test updating user info"""
    response = await client.put(
        "/api/auth/me",
        headers=auth_headers,
        json={"name": "Updated Name"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
