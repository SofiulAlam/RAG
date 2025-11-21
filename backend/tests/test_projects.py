import pytest
from httpx import AsyncClient
from app.models.user import User


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient, auth_headers):
    """Test creating a new project"""
    response = await client.post(
        "/api/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "framework": "Next.js",
            "project_prompt": "Build a todo app"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["framework"] == "Next.js"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient, auth_headers):
    """Test listing user's projects"""
    # Create a project first
    await client.post(
        "/api/projects",
        headers=auth_headers,
        json={"name": "Project 1", "framework": "Next.js"}
    )

    # List projects
    response = await client.get(
        "/api/projects",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient, auth_headers):
    """Test getting a specific project"""
    # Create project
    create_response = await client.post(
        "/api/projects",
        headers=auth_headers,
        json={"name": "Test Project", "framework": "Next.js"}
    )
    project_id = create_response.json()["id"]

    # Get project
    response = await client.get(
        f"/api/projects/{project_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == "Test Project"


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient, auth_headers):
    """Test updating a project"""
    # Create project
    create_response = await client.post(
        "/api/projects",
        headers=auth_headers,
        json={"name": "Test Project", "framework": "Next.js"}
    )
    project_id = create_response.json()["id"]

    # Update project
    response = await client.put(
        f"/api/projects/{project_id}",
        headers=auth_headers,
        json={"name": "Updated Project"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Project"


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient, auth_headers):
    """Test deleting a project"""
    # Create project
    create_response = await client.post(
        "/api/projects",
        headers=auth_headers,
        json={"name": "Test Project", "framework": "Next.js"}
    )
    project_id = create_response.json()["id"]

    # Delete project
    response = await client.delete(
        f"/api/projects/{project_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    # Verify deleted
    get_response = await client.get(
        f"/api/projects/{project_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing projects without authentication"""
    response = await client.get("/api/projects")
    assert response.status_code == 403  # Forbidden without auth
