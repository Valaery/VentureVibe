import pytest
from unittest.mock import Mock, AsyncMock
from src.application.use_cases.workflow_service import WorkflowService
from src.domain.entities import ProductIdea, ResearchResult
from src.domain.value_objects import FeasibilityScore

class TestWorkflowService:
    @pytest.fixture
    def mock_idea_repo(self):
        return AsyncMock()

    @pytest.fixture
    def mock_result_repo(self):
        return AsyncMock()

    @pytest.fixture
    def mock_agent_service(self):
        return AsyncMock()

    @pytest.fixture
    def workflow_service(self, mock_idea_repo, mock_result_repo, mock_agent_service):
        return WorkflowService(mock_idea_repo, mock_result_repo, mock_agent_service)

    async def test_run_research_success(self, workflow_service, mock_idea_repo, mock_result_repo, mock_agent_service):
        # Arrange
        user_id = "user_123"
        content = "My Great Product Idea"
        target_audience = "Everyone"
        
        mock_agent_service.get_strategy.return_value = "Strategic Plan"
        mock_agent_service.analyze_market.return_value = {
            "market_analysis": "Great market",
            "feasibility_score": FeasibilityScore(root=80),
            "competitors": ["Comp1"],
            "strategic_advice": "Do it"
        }
        
        # Act
        result = await workflow_service.run_research(user_id, content, target_audience)

        # Assert
        assert isinstance(result, ResearchResult)
        assert result.market_analysis == "Great market"
        assert int(result.feasibility_score) == 80
        
        # Verify repository calls
        mock_idea_repo.create.assert_called_once()
        mock_result_repo.create.assert_called_once()
        
        # Verify agent service calls
        mock_agent_service.get_strategy.assert_called_once_with(content, target_audience)
        mock_agent_service.analyze_market.assert_called_once_with(content, "Strategic Plan")

    async def test_get_result(self, workflow_service, mock_result_repo):
        # Arrange
        result_id = "res_123"
        expected_result = Mock(spec=ResearchResult)
        mock_result_repo.get_by_idea_id.return_value = expected_result

        # Act
        result = await workflow_service.get_result(result_id)

        # Assert
        assert result == expected_result
        mock_result_repo.get_by_idea_id.assert_called_once_with(result_id)
