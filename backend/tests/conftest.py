import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import create_app
from src.infrastructure.web.dependencies import get_user_repository, get_workflow_service
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_user_repo():
    repo = MagicMock()
    users_db = {}
    
    async def create(user):
        # Store user in the "db" using email as key
        # We need to simulate that the object returned has attributes like access via dot notation if it's an object,
        # or just store the object itself. 
        # The Application (AuthService) creates a User entity.
        # The repo.create method receives a User entity.
        users_db[str(user.email)] = user
        return user
        
    async def get_by_email(email):
        return users_db.get(str(email))

    repo.create = AsyncMock(side_effect=create)
    repo.get_by_email = AsyncMock(side_effect=get_by_email)
    return repo

@pytest.fixture
def mock_workflow_service():
    service = MagicMock()
    service.run_research = AsyncMock(return_value={
        "id": "res_123",
        "idea_id": "idea_123",
        "market_analysis": "Analysis",
        "feasibility_score": 85,
        "competitors": ["Comp A"],
        "strategic_advice": "Do it",
        "agent_thoughts": []
    })
    return service

@pytest_asyncio.fixture
async def client(mock_user_repo, mock_workflow_service):
    app = create_app()
    app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    app.dependency_overrides[get_workflow_service] = lambda: mock_workflow_service
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
