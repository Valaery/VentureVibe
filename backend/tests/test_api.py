import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    token = await get_auth_token(client)
    assert token is not None

async def get_auth_token(client: AsyncClient) -> str:
    # Register
    register_res = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    # If user already exists (from previous tests sharing state?), handle it or assert 200/400
    # With stateful mock repo, it persists? No, scope is function/default, but wait.
    # mock_user_repo fixture scope is default (function). So new repo for each test.
    
    assert register_res.status_code in [200, 400] 

    # Login
    login_res = await client.post("/auth/token", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    return token_data["access_token"]

@pytest.mark.asyncio
async def test_research_flow(client: AsyncClient):
    # First get token
    token = await get_auth_token(client)
    
    # Request Research
    res = await client.post(
        "/research/", 
        json={"content": "A smart coffee mug", "target_audience": "Techies"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "res_123"
    assert data["feasibility_score"] == 85
