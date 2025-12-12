import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.infrastructure.adapters.agent_adapter import PydanticAgentAdapter, MarketAnalysisResponse

class TestPydanticAgentAdapter:
    @pytest.fixture
    def mock_agent_cls(self):
        with patch('src.infrastructure.adapters.agent_adapter.Agent') as mock:
            yield mock

    @pytest.fixture
    def adapter(self, mock_agent_cls):
        return PydanticAgentAdapter()

    async def test_get_strategy(self, adapter, mock_agent_cls):
        # Arrange
        mock_result = Mock()
        mock_result.data = "Strategic Plan"
        
        adapter.strategist_agent.run = AsyncMock(return_value=mock_result)

        # Act
        result = await adapter.get_strategy("Idea", "Audience")

        # Assert
        assert result == "Strategic Plan"
        adapter.strategist_agent.run.assert_called_once()
        assert "Idea" in adapter.strategist_agent.run.call_args[0][0]

    async def test_get_strategy_retry_success(self, adapter):
        # Arrange
        mock_result = Mock()
        mock_result.data = "Strategic Plan"
        
        # First call raises exception, second succeeds
        adapter.strategist_agent.run = AsyncMock(side_effect=[Exception("Fail"), mock_result])

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            # Act
            result = await adapter.get_strategy("Idea", "Audience")

            # Assert
            assert result == "Strategic Plan"
            assert adapter.strategist_agent.run.call_count == 2
            mock_sleep.assert_called_once()

    async def test_get_strategy_retry_failure(self, adapter):
        # Arrange
        adapter.strategist_agent.run = AsyncMock(side_effect=Exception("Fail"))

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            # Act & Assert
            with pytest.raises(Exception, match="Fail"):
                await adapter.get_strategy("Idea", "Audience")
            
            assert adapter.strategist_agent.run.call_count == 3
            assert mock_sleep.call_count == 3 # 3 fails -> 3 sleeps? Loop: 0..3. 
            # for attempt in range(3):
            #   try...
            #   except... sleep...
            # If all 3 fail, it sleeps 3 times then raises. Yes.

    async def test_analyze_market(self, adapter):
        # Arrange
        response_model = MarketAnalysisResponse(
            market_analysis="Analysis",
            feasibility_score=80,
            competitors=["Comp"],
            strategic_advice="Advice"
        )
        mock_result = Mock()
        mock_result.data = response_model
        
        adapter.analyst_agent.run = AsyncMock(return_value=mock_result)

        # Act
        result = await adapter.analyze_market("Idea", "Strategy")

        # Assert
        assert result['market_analysis'] == "Analysis"
        assert result['feasibility_score'] == 80
        adapter.analyst_agent.run.assert_called_once()
