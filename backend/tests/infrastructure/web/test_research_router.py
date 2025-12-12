import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from src.main import app
from src.infrastructure.web.dependencies import get_workflow_service, get_current_user
from src.domain.entities import User, ResearchResult
from src.domain.value_objects import Email, HashedPassword, FeasibilityScore
from src.infrastructure.web.dtos.schemas import ResearchRequest

client = TestClient(app)

class TestResearchRouter:
    @pytest.fixture
    def mock_workflow_service(self):
        return AsyncMock()

    @pytest.fixture
    def mock_user(self):
        return User(
            id="user_123",
            email=Email(root="test@example.com"),
            hashed_password=HashedPassword(root="hashed")
        )

    @pytest.fixture
    def override_dependencies(self, mock_workflow_service, mock_user):
        app.dependency_overrides[get_workflow_service] = lambda: mock_workflow_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        yield
        app.dependency_overrides = {}

    def test_create_research_success(self, override_dependencies, mock_workflow_service, mock_user):
        # Arrange
        payload = {
            "content": "My Idea",
            "target_audience": "Audience"
        }
        mock_result = ResearchResult(
            idea_id="idea_123",
            market_analysis="Analysis",
            feasibility_score=FeasibilityScore(root=85),
            competitors=["Comp1"],
            strategic_advice="Advice"
        )
        mock_workflow_service.run_research.return_value = mock_result

        # Act
        response = client.post("/research/", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["idea_id"] == "idea_123"
        assert data["feasibility_score"] == 85
        mock_workflow_service.run_research.assert_called_once_with("user_123", "My Idea", "Audience")

    def test_get_research_success(self, override_dependencies, mock_workflow_service, mock_user):
        # Arrange
        idea_id = "idea_123"
        mock_result = ResearchResult(
            idea_id=idea_id,
            market_analysis="Analysis",
            feasibility_score=FeasibilityScore(root=85),
            competitors=["Comp1"],
            strategic_advice="Advice"
        )
        mock_workflow_service.get_result.return_value = mock_result

        # Act
        response = client.get(f"/research/{idea_id}")

        # Assert
        assert response.status_code == 200
        assert response.json()["idea_id"] == idea_id
        mock_workflow_service.get_result.assert_called_once_with(idea_id)

    def test_get_research_not_found(self, override_dependencies, mock_workflow_service, mock_user):
        # Arrange
        mock_workflow_service.get_result.return_value = None

        # Act
        response = client.get("/research/unknown_id")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Research not found"
