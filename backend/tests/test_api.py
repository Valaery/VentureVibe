import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register
    register_res = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert register_res.status_code == 200
    data = register_res.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

    # Login
    login_res = await client.post("/auth/token", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    return token_data["access_token"]

@pytest.mark.asyncio
async def test_research_flow(client: AsyncClient):
    # First get token
    token = await test_register_and_login(client)
    
    # Request Research
    res = await client.post(
        "/research/", 
        json={"content": "A smart coffee mug", "target_audience": "Techies"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "123"
    assert data["feasibility_score"] == 85
