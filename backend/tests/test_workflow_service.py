# ABOUTME: Unit tests for WorkflowService orchestrating the 6-agent research pipeline.
# ABOUTME: Tests parallel execution via asyncio.gather, result assembly, and error handling.

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.application.use_cases.workflow_service import WorkflowService
from src.domain.entities import (
    ProductIdea,
    ResearchResult,
    MarketSizing,
    Competitor,
    CompetitiveAnalysis,
    SWOTAnalysis,
    RiskFactor,
    GTMStrategy,
    AgentThought
)


class TestWorkflowService:
    """Test suite for WorkflowService pipeline orchestration."""

    @pytest.fixture
    def mock_idea_repository(self):
        """Mock ProductIdeaRepository."""
        repo = MagicMock()
        repo.create = AsyncMock(return_value=None)
        return repo

    @pytest.fixture
    def mock_result_repository(self):
        """Mock ResearchResultRepository."""
        repo = MagicMock()
        repo.create = AsyncMock(return_value=None)
        return repo

    @pytest.fixture
    def mock_agent_service(self):
        """Mock AgentService with all 6 methods."""
        service = MagicMock()

        # Phase 1: Strategist
        service.get_strategy = AsyncMock(
            return_value="Strategic direction: Focus on SMB SaaS market with PLG approach."
        )

        # Phase 2: Parallel agents
        service.analyze_market = AsyncMock(return_value={
            'executive_summary': 'Viable product with strong market potential.',
            'market_analysis': 'Growing market with 15% CAGR.',
            'strategic_advice': 'Start with freemium model.',
            'feasibility_score': 75,
            'confidence_level': 'high',
            'investment_readiness': 'mvp_ready',
            'key_assumptions': ['Assumption 1', 'Assumption 2'],
            'recommended_next_steps': ['Build MVP', 'Talk to 10 customers']
        })

        service.size_market = AsyncMock(return_value=MarketSizing(
            tam_usd_billion=100.0,
            sam_usd_billion=25.0,
            som_usd_million=500.0,
            sizing_methodology="top_down",
            tam_source_basis="Gartner Report 2025"
        ))

        service.analyze_competitors = AsyncMock(return_value=CompetitiveAnalysis(
            direct_competitors=[
                Competitor(
                    name="CompetitorX",
                    positioning="Enterprise automation",
                    primary_weakness="Complex setup",
                    business_model="B2B SaaS"
                )
            ],
            indirect_competitors=[],
            competitive_moat="Network effects and proprietary data",
            differentiation_score=8
        ))

        service.analyze_swot_risks = AsyncMock(return_value={
            'swot': SWOTAnalysis(
                strengths=['Strong technical team', 'First mover'],
                weaknesses=['No sales team'],
                opportunities=['Market growth'],
                threats=['Incumbent competition']
            ),
            'risks': [
                RiskFactor(
                    category='technical',
                    description='API dependency risk',
                    severity='high',
                    mitigation='Build fallback provider'
                )
            ]
        })

        service.develop_gtm = AsyncMock(return_value=GTMStrategy(
            primary_channel="Product-led freemium",
            secondary_channels=["SEO", "Content marketing"],
            pricing_model="Freemium (free up to 100 users, $49/mo Pro)",
            estimated_cac_usd=250.0,
            target_icp="Series A SaaS companies with 20-100 employees",
            time_to_first_revenue_months=3
        ))

        return service

    @pytest.fixture
    def workflow_service(self, mock_idea_repository, mock_result_repository, mock_agent_service):
        """Create WorkflowService instance with mocked dependencies."""
        return WorkflowService(
            idea_repository=mock_idea_repository,
            result_repository=mock_result_repository,
            agent_service=mock_agent_service
        )

    @pytest.mark.asyncio
    async def test_execute_research_creates_product_idea(
        self,
        workflow_service,
        mock_idea_repository
    ):
        """Test execute_research creates and persists ProductIdea."""
        user_id = "user_123"
        content = "A smart coffee mug that tracks hydration"
        target_audience = "Health-conscious professionals"

        await workflow_service.execute_research(user_id, content, target_audience)

        # Verify idea was created
        mock_idea_repository.create.assert_called_once()
        created_idea = mock_idea_repository.create.call_args[0][0]

        assert isinstance(created_idea, ProductIdea)
        assert created_idea.user_id == user_id
        assert created_idea.content == content
        assert created_idea.target_audience == target_audience

    @pytest.mark.asyncio
    async def test_execute_research_calls_strategist_first(
        self,
        workflow_service,
        mock_agent_service
    ):
        """Test execute_research calls get_strategy in Phase 1."""
        user_id = "user_123"
        content = "AI-powered code review tool"
        target_audience = "Software development teams"

        await workflow_service.execute_research(user_id, content, target_audience)

        # Verify strategist was called with correct arguments
        mock_agent_service.get_strategy.assert_called_once_with(content, target_audience)

    @pytest.mark.asyncio
    @patch('src.application.use_cases.workflow_service.asyncio.gather', new_callable=AsyncMock)
    async def test_execute_research_calls_parallel_agents_with_gather(
        self,
        mock_gather,
        workflow_service,
        mock_agent_service
    ):
        """Test execute_research uses asyncio.gather for Phase 2 parallel execution."""
        # Setup mock gather to return expected results (as an awaitable)
        mock_gather.return_value = (
            mock_agent_service.analyze_market.return_value,
            mock_agent_service.size_market.return_value,
            mock_agent_service.analyze_competitors.return_value,
            mock_agent_service.analyze_swot_risks.return_value,
            mock_agent_service.develop_gtm.return_value
        )

        user_id = "user_123"
        content = "Smart home energy optimizer"
        target_audience = "Homeowners"

        await workflow_service.execute_research(user_id, content, target_audience)

        # Verify asyncio.gather was called (5 agents in parallel)
        mock_gather.assert_called_once()

        # Verify all 5 specialist agents were called with strategy
        strategy = await mock_agent_service.get_strategy(content, target_audience)
        mock_agent_service.analyze_market.assert_called_once_with(content, strategy)
        mock_agent_service.size_market.assert_called_once_with(content, strategy)
        mock_agent_service.analyze_competitors.assert_called_once_with(content, strategy)
        mock_agent_service.analyze_swot_risks.assert_called_once_with(content, strategy)
        mock_agent_service.develop_gtm.assert_called_once_with(content, strategy)

    @pytest.mark.asyncio
    async def test_execute_research_assembles_research_result_correctly(
        self,
        workflow_service,
        mock_result_repository
    ):
        """Test execute_research correctly assembles ResearchResult from agent outputs."""
        user_id = "user_123"
        content = "B2B invoice automation platform"
        target_audience = "SMB finance teams"

        result = await workflow_service.execute_research(user_id, content, target_audience)

        # Verify result is a ResearchResult instance
        assert isinstance(result, ResearchResult)

        # Verify all narrative fields from analyst
        assert result.executive_summary == 'Viable product with strong market potential.'
        assert result.market_analysis == 'Growing market with 15% CAGR.'
        assert result.strategic_advice == 'Start with freemium model.'

        # Verify score fields
        assert result.feasibility_score == 75
        assert result.confidence_level == 'high'
        assert result.investment_readiness == 'mvp_ready'

        # Verify list fields
        assert result.key_assumptions == ['Assumption 1', 'Assumption 2']
        assert result.recommended_next_steps == ['Build MVP', 'Talk to 10 customers']

        # Verify sub-entities
        assert isinstance(result.market_sizing, MarketSizing)
        assert result.market_sizing.tam_usd_billion == 100.0

        assert isinstance(result.competitive_analysis, CompetitiveAnalysis)
        assert len(result.competitive_analysis.direct_competitors) == 1

        assert isinstance(result.swot_analysis, SWOTAnalysis)
        assert len(result.swot_analysis.strengths) == 2

        assert isinstance(result.risk_factors, list)
        assert len(result.risk_factors) == 1
        assert result.risk_factors[0].severity == 'high'

        assert isinstance(result.gtm_strategy, GTMStrategy)
        assert result.gtm_strategy.primary_channel == "Product-led freemium"

        # Verify agent thoughts populated
        assert len(result.agent_thoughts) == 6
        assert result.agent_thoughts[0].agent_name == "Product Strategist"

    @pytest.mark.asyncio
    async def test_execute_research_persists_research_result(
        self,
        workflow_service,
        mock_result_repository
    ):
        """Test execute_research persists ResearchResult to repository."""
        user_id = "user_123"
        content = "Mobile app for plant care reminders"
        target_audience = "Urban gardeners"

        result = await workflow_service.execute_research(user_id, content, target_audience)

        # Verify result was saved
        mock_result_repository.create.assert_called_once()
        saved_result = mock_result_repository.create.call_args[0][0]

        assert isinstance(saved_result, ResearchResult)
        assert saved_result.id == result.id
        assert saved_result.executive_summary == result.executive_summary

    @pytest.mark.asyncio
    async def test_execute_research_returns_complete_result(
        self,
        workflow_service
    ):
        """Test execute_research returns complete ResearchResult with all fields."""
        user_id = "user_123"
        content = "AI-powered customer support chatbot"
        target_audience = "E-commerce companies"

        result = await workflow_service.execute_research(user_id, content, target_audience)

        # Verify all required fields are present and not None
        assert result.id is not None
        assert result.idea_id is not None
        assert result.executive_summary is not None
        assert result.market_analysis is not None
        assert result.strategic_advice is not None
        assert result.key_assumptions is not None
        assert result.recommended_next_steps is not None
        assert result.feasibility_score is not None
        assert result.confidence_level is not None
        assert result.investment_readiness is not None
        assert result.market_sizing is not None
        assert result.competitive_analysis is not None
        assert result.swot_analysis is not None
        assert result.risk_factors is not None
        assert result.gtm_strategy is not None
        assert result.agent_thoughts is not None
        assert result.created_at is not None

    @pytest.mark.asyncio
    async def test_execute_research_agent_thoughts_order(
        self,
        workflow_service
    ):
        """Test execute_research populates agent_thoughts in correct order."""
        user_id = "user_123"
        content = "SaaS platform for remote team collaboration"
        target_audience = "Remote-first companies"

        result = await workflow_service.execute_research(user_id, content, target_audience)

        # Verify agent thoughts are in expected order
        expected_agents = [
            "Product Strategist",
            "Research Analyst",
            "Market Sizing Analyst",
            "Competitive Intelligence Analyst",
            "SWOT & Risk Analyst",
            "GTM Strategist"
        ]

        assert len(result.agent_thoughts) == 6
        for i, expected_name in enumerate(expected_agents):
            assert result.agent_thoughts[i].agent_name == expected_name
            assert isinstance(result.agent_thoughts[i], AgentThought)
            assert result.agent_thoughts[i].thought is not None

    @pytest.mark.asyncio
    async def test_execute_research_with_minimal_target_audience(
        self,
        workflow_service,
        mock_agent_service
    ):
        """Test execute_research handles empty or minimal target_audience."""
        user_id = "user_123"
        content = "Blockchain-based supply chain tracker"
        target_audience = ""

        await workflow_service.execute_research(user_id, content, target_audience)

        # Verify strategist still called with empty audience
        mock_agent_service.get_strategy.assert_called_once_with(content, target_audience)

    @pytest.mark.asyncio
    async def test_get_result_retrieves_from_repository(
        self,
        workflow_service,
        mock_result_repository
    ):
        """Test get_result retrieves ResearchResult from repository by idea ID."""
        result_id = "idea_123"
        expected_result = MagicMock(spec=ResearchResult)
        mock_result_repository.get_by_idea_id = AsyncMock(return_value=expected_result)

        result = await workflow_service.get_result(result_id)

        mock_result_repository.get_by_idea_id.assert_called_once_with(result_id)
        assert result == expected_result

    @pytest.mark.asyncio
    async def test_get_result_returns_none_when_not_found(
        self,
        workflow_service,
        mock_result_repository
    ):
        """Test get_result returns None when result not found in repository."""
        result_id = "nonexistent_id"
        mock_result_repository.get_by_idea_id = AsyncMock(return_value=None)

        result = await workflow_service.get_result(result_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_execute_research_handles_analyst_dict_structure(
        self,
        workflow_service,
        mock_agent_service
    ):
        """Test execute_research correctly unpacks dict from analyze_market."""
        user_id = "user_123"
        content = "AI writing assistant for legal documents"
        target_audience = "Law firms"

        # Verify mock returns dict
        analyst_output = await mock_agent_service.analyze_market(content, "strategy")
        assert isinstance(analyst_output, dict)
        assert 'executive_summary' in analyst_output
        assert 'market_analysis' in analyst_output
        assert 'strategic_advice' in analyst_output

        result = await workflow_service.execute_research(user_id, content, target_audience)

        # Verify dict fields were correctly assigned to ResearchResult
        assert result.executive_summary == analyst_output['executive_summary']
        assert result.market_analysis == analyst_output['market_analysis']
        assert result.strategic_advice == analyst_output['strategic_advice']
        assert result.feasibility_score == analyst_output['feasibility_score']
        assert result.confidence_level == analyst_output['confidence_level']
        assert result.investment_readiness == analyst_output['investment_readiness']

    @pytest.mark.asyncio
    async def test_execute_research_handles_swot_risk_dict_structure(
        self,
        workflow_service,
        mock_agent_service
    ):
        """Test execute_research correctly unpacks dict from analyze_swot_risks."""
        user_id = "user_123"
        content = "Peer-to-peer car rental marketplace"
        target_audience = "Car owners and renters"

        # Verify mock returns dict with 'swot' and 'risks' keys
        swot_risk_output = await mock_agent_service.analyze_swot_risks(content, "strategy")
        assert isinstance(swot_risk_output, dict)
        assert 'swot' in swot_risk_output
        assert 'risks' in swot_risk_output

        result = await workflow_service.execute_research(user_id, content, target_audience)

        # Verify dict fields were correctly assigned to ResearchResult
        assert result.swot_analysis == swot_risk_output['swot']
        assert result.risk_factors == swot_risk_output['risks']

    @pytest.mark.asyncio
    async def test_execute_research_exception_propagates(
        self,
        workflow_service,
        mock_agent_service
    ):
        """Test execute_research propagates exceptions from agent service."""
        user_id = "user_123"
        content = "VR fitness app"
        target_audience = "Fitness enthusiasts"

        # Simulate agent failure
        mock_agent_service.size_market.side_effect = Exception("API rate limit exceeded")

        with pytest.raises(Exception) as exc_info:
            await workflow_service.execute_research(user_id, content, target_audience)

        assert "API rate limit exceeded" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_research_logs_progress(
        self,
        workflow_service,
        caplog
    ):
        """Test execute_research logs progress at key phases."""
        import logging
        caplog.set_level(logging.INFO)

        user_id = "user_123"
        content = "B2B procurement automation software"
        target_audience = "Enterprise procurement teams"

        await workflow_service.execute_research(user_id, content, target_audience)

        # Verify key log messages
        log_messages = [record.message for record in caplog.records]

        assert any("Created product idea" in msg for msg in log_messages)
        assert any("Phase 1: Running Product Strategist" in msg for msg in log_messages)
        assert any("Product Strategist completed" in msg for msg in log_messages)
        assert any("Phase 2: Running 5 specialist agents in parallel" in msg for msg in log_messages)
        assert any("All 5 specialist agents completed" in msg for msg in log_messages)
        assert any("Research result" in msg and "saved" in msg for msg in log_messages)
