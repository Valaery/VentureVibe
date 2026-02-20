# ABOUTME: Unit tests for domain entities in the pipeline-enhancement feature.
# ABOUTME: Tests validation, instantiation, and field constraints for all 6 new models plus ResearchResult.

import pytest
from datetime import datetime
from pydantic import ValidationError
from src.domain.entities import (
    MarketSizing,
    Competitor,
    CompetitiveAnalysis,
    SWOTAnalysis,
    RiskFactor,
    GTMStrategy,
    ResearchResult,
    AgentThought,
    ProductIdea
)


class TestMarketSizing:
    """Test suite for MarketSizing entity."""

    def test_market_sizing_valid_top_down(self):
        """Test MarketSizing instantiation with valid top_down methodology."""
        market_sizing = MarketSizing(
            tam_usd_billion=100.5,
            sam_usd_billion=25.2,
            som_usd_million=500.0,
            sizing_methodology="top_down",
            tam_source_basis="Gartner Report 2025",
            growth_rate_pct=15.5
        )

        assert market_sizing.tam_usd_billion == 100.5
        assert market_sizing.sam_usd_billion == 25.2
        assert market_sizing.som_usd_million == 500.0
        assert market_sizing.sizing_methodology == "top_down"
        assert market_sizing.tam_source_basis == "Gartner Report 2025"
        assert market_sizing.growth_rate_pct == 15.5

    def test_market_sizing_valid_bottom_up(self):
        """Test MarketSizing instantiation with valid bottom_up methodology."""
        market_sizing = MarketSizing(
            tam_usd_billion=50.0,
            sam_usd_billion=10.0,
            som_usd_million=200.0,
            sizing_methodology="bottom_up",
            tam_source_basis="Unit economics calculation"
        )

        assert market_sizing.sizing_methodology == "bottom_up"
        assert market_sizing.growth_rate_pct is None

    def test_market_sizing_valid_hybrid(self):
        """Test MarketSizing instantiation with valid hybrid methodology."""
        market_sizing = MarketSizing(
            tam_usd_billion=75.0,
            sam_usd_billion=18.0,
            som_usd_million=350.0,
            sizing_methodology="hybrid",
            tam_source_basis="Cross-validated top-down and bottom-up"
        )

        assert market_sizing.sizing_methodology == "hybrid"

    def test_market_sizing_invalid_methodology(self):
        """Test MarketSizing raises error for invalid methodology."""
        with pytest.raises(ValidationError) as exc_info:
            MarketSizing(
                tam_usd_billion=100.0,
                sam_usd_billion=25.0,
                som_usd_million=500.0,
                sizing_methodology="invalid_method",
                tam_source_basis="Some source"
            )

        assert "sizing_methodology" in str(exc_info.value)

    def test_market_sizing_missing_required_fields(self):
        """Test MarketSizing raises error when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            MarketSizing(
                tam_usd_billion=100.0,
                sam_usd_billion=25.0
            )

        assert "som_usd_million" in str(exc_info.value)
        assert "sizing_methodology" in str(exc_info.value)
        assert "tam_source_basis" in str(exc_info.value)


class TestCompetitor:
    """Test suite for Competitor entity."""

    def test_competitor_valid_with_funding(self):
        """Test Competitor instantiation with all fields including funding."""
        competitor = Competitor(
            name="CompanyX",
            positioning="Enterprise AI automation platform",
            primary_weakness="Complex setup, 2-week onboarding",
            estimated_funding_usd_million=150.5,
            business_model="B2B SaaS"
        )

        assert competitor.name == "CompanyX"
        assert competitor.positioning == "Enterprise AI automation platform"
        assert competitor.primary_weakness == "Complex setup, 2-week onboarding"
        assert competitor.estimated_funding_usd_million == 150.5
        assert competitor.business_model == "B2B SaaS"

    def test_competitor_valid_without_funding(self):
        """Test Competitor instantiation without optional funding field."""
        competitor = Competitor(
            name="StartupY",
            positioning="SMB workflow automation",
            primary_weakness="Limited feature set",
            business_model="Freemium"
        )

        assert competitor.name == "StartupY"
        assert competitor.estimated_funding_usd_million is None

    def test_competitor_missing_required_fields(self):
        """Test Competitor raises error when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            Competitor(
                name="CompanyZ",
                positioning="Some positioning"
            )

        assert "primary_weakness" in str(exc_info.value)
        assert "business_model" in str(exc_info.value)


class TestCompetitiveAnalysis:
    """Test suite for CompetitiveAnalysis entity."""

    def test_competitive_analysis_valid(self):
        """Test CompetitiveAnalysis instantiation with valid competitor lists."""
        direct = [
            Competitor(
                name="DirectComp1",
                positioning="Same problem, same approach",
                primary_weakness="Expensive pricing",
                business_model="B2B SaaS"
            ),
            Competitor(
                name="DirectComp2",
                positioning="Similar solution",
                primary_weakness="Poor UX",
                business_model="Enterprise"
            )
        ]

        indirect = [
            Competitor(
                name="IndirectComp1",
                positioning="Different approach, same problem",
                primary_weakness="Manual process",
                business_model="Consulting"
            )
        ]

        competitive_analysis = CompetitiveAnalysis(
            direct_competitors=direct,
            indirect_competitors=indirect,
            competitive_moat="Network effects and proprietary ML model",
            differentiation_score=8
        )

        assert len(competitive_analysis.direct_competitors) == 2
        assert len(competitive_analysis.indirect_competitors) == 1
        assert competitive_analysis.competitive_moat == "Network effects and proprietary ML model"
        assert competitive_analysis.differentiation_score == 8

    def test_competitive_analysis_differentiation_score_boundary(self):
        """Test CompetitiveAnalysis accepts valid differentiation scores 1-10."""
        for score in [1, 5, 10]:
            analysis = CompetitiveAnalysis(
                direct_competitors=[],
                indirect_competitors=[],
                competitive_moat="Some moat",
                differentiation_score=score
            )
            assert analysis.differentiation_score == score

    def test_competitive_analysis_empty_lists(self):
        """Test CompetitiveAnalysis allows empty competitor lists."""
        analysis = CompetitiveAnalysis(
            direct_competitors=[],
            indirect_competitors=[],
            competitive_moat="First mover advantage",
            differentiation_score=9
        )

        assert len(analysis.direct_competitors) == 0
        assert len(analysis.indirect_competitors) == 0


class TestSWOTAnalysis:
    """Test suite for SWOTAnalysis entity."""

    def test_swot_analysis_valid(self):
        """Test SWOTAnalysis instantiation with all quadrants populated."""
        swot = SWOTAnalysis(
            strengths=["Strong technical team", "First mover in regulated space", "Patent pending"],
            weaknesses=["No sales team", "Limited budget", "Requires regulatory approval"],
            opportunities=["New regulation Q3 2026", "Market consolidation", "Partner ecosystem"],
            threats=["Incumbent X launched competing feature", "Economic downturn", "Tech talent shortage"]
        )

        assert len(swot.strengths) == 3
        assert len(swot.weaknesses) == 3
        assert len(swot.opportunities) == 3
        assert len(swot.threats) == 3
        assert "Strong technical team" in swot.strengths
        assert "No sales team" in swot.weaknesses

    def test_swot_analysis_empty_quadrants(self):
        """Test SWOTAnalysis allows empty lists for any quadrant."""
        swot = SWOTAnalysis(
            strengths=["Only strength"],
            weaknesses=[],
            opportunities=[],
            threats=[]
        )

        assert len(swot.strengths) == 1
        assert len(swot.weaknesses) == 0
        assert len(swot.opportunities) == 0
        assert len(swot.threats) == 0

    def test_swot_analysis_missing_required_fields(self):
        """Test SWOTAnalysis raises error when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            SWOTAnalysis(
                strengths=["Strength"],
                weaknesses=["Weakness"]
            )

        assert "opportunities" in str(exc_info.value)
        assert "threats" in str(exc_info.value)


class TestRiskFactor:
    """Test suite for RiskFactor entity."""

    def test_risk_factor_valid_all_categories(self):
        """Test RiskFactor instantiation with all valid categories."""
        categories = ["market", "technical", "regulatory", "competitive", "financial", "execution"]

        for category in categories:
            risk = RiskFactor(
                category=category,
                description="Test risk description",
                severity="high",
                mitigation="Test mitigation strategy"
            )
            assert risk.category == category

    def test_risk_factor_valid_all_severities(self):
        """Test RiskFactor instantiation with all valid severity levels."""
        severities = ["low", "medium", "high", "critical"]

        for severity in severities:
            risk = RiskFactor(
                category="technical",
                description="Test risk",
                severity=severity,
                mitigation="Test mitigation"
            )
            assert risk.severity == severity

    def test_risk_factor_invalid_category(self):
        """Test RiskFactor raises error for invalid category."""
        with pytest.raises(ValidationError) as exc_info:
            RiskFactor(
                category="invalid_category",
                description="Test risk",
                severity="high",
                mitigation="Test mitigation"
            )

        assert "category" in str(exc_info.value)

    def test_risk_factor_invalid_severity(self):
        """Test RiskFactor raises error for invalid severity."""
        with pytest.raises(ValidationError) as exc_info:
            RiskFactor(
                category="technical",
                description="Test risk",
                severity="extreme",
                mitigation="Test mitigation"
            )

        assert "severity" in str(exc_info.value)

    def test_risk_factor_critical_severity(self):
        """Test RiskFactor with critical severity for business-ending risks."""
        risk = RiskFactor(
            category="technical",
            description="Core API dependency has no fallback, failure means total outage",
            severity="critical",
            mitigation="Build abstraction layer supporting 3 providers"
        )

        assert risk.severity == "critical"
        assert "no fallback" in risk.description


class TestGTMStrategy:
    """Test suite for GTMStrategy entity."""

    def test_gtm_strategy_valid_with_cac(self):
        """Test GTMStrategy instantiation with all fields including CAC."""
        gtm = GTMStrategy(
            primary_channel="Product-led freemium",
            secondary_channels=["SEO + content", "LinkedIn organic"],
            pricing_model="Freemium (free up to 100 users, $49/mo Pro)",
            estimated_cac_usd=250.0,
            target_icp="Series A-B SaaS companies (20-100 employees) with $2M-$10M ARR",
            time_to_first_revenue_months=3
        )

        assert gtm.primary_channel == "Product-led freemium"
        assert len(gtm.secondary_channels) == 2
        assert gtm.pricing_model == "Freemium (free up to 100 users, $49/mo Pro)"
        assert gtm.estimated_cac_usd == 250.0
        assert "Series A-B SaaS" in gtm.target_icp
        assert gtm.time_to_first_revenue_months == 3

    def test_gtm_strategy_valid_without_cac(self):
        """Test GTMStrategy instantiation without optional CAC field."""
        gtm = GTMStrategy(
            primary_channel="Enterprise sales",
            secondary_channels=["Partnerships", "Events"],
            pricing_model="Annual contract ($50K-$200K)",
            target_icp="Fortune 500 financial services companies",
            time_to_first_revenue_months=12
        )

        assert gtm.primary_channel == "Enterprise sales"
        assert gtm.estimated_cac_usd is None
        assert gtm.time_to_first_revenue_months == 12

    def test_gtm_strategy_empty_secondary_channels(self):
        """Test GTMStrategy allows empty secondary channels list."""
        gtm = GTMStrategy(
            primary_channel="Community-led",
            secondary_channels=[],
            pricing_model="Usage-based ($0.10 per API call)",
            target_icp="Developer tools startups",
            time_to_first_revenue_months=2
        )

        assert len(gtm.secondary_channels) == 0

    def test_gtm_strategy_missing_required_fields(self):
        """Test GTMStrategy raises error when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            GTMStrategy(
                primary_channel="SEO",
                secondary_channels=["Social media"]
            )

        assert "pricing_model" in str(exc_info.value)
        assert "target_icp" in str(exc_info.value)
        assert "time_to_first_revenue_months" in str(exc_info.value)


class TestResearchResult:
    """Test suite for ResearchResult entity with all sub-models."""

    @pytest.fixture
    def valid_market_sizing(self):
        """Fixture for valid MarketSizing."""
        return MarketSizing(
            tam_usd_billion=100.0,
            sam_usd_billion=25.0,
            som_usd_million=500.0,
            sizing_methodology="top_down",
            tam_source_basis="Industry report"
        )

    @pytest.fixture
    def valid_competitive_analysis(self):
        """Fixture for valid CompetitiveAnalysis."""
        return CompetitiveAnalysis(
            direct_competitors=[
                Competitor(
                    name="Competitor1",
                    positioning="Similar solution",
                    primary_weakness="Expensive",
                    business_model="B2B SaaS"
                )
            ],
            indirect_competitors=[],
            competitive_moat="Network effects",
            differentiation_score=7
        )

    @pytest.fixture
    def valid_swot_analysis(self):
        """Fixture for valid SWOTAnalysis."""
        return SWOTAnalysis(
            strengths=["Strong team"],
            weaknesses=["No funding"],
            opportunities=["Market growth"],
            threats=["Competition"]
        )

    @pytest.fixture
    def valid_risk_factors(self):
        """Fixture for valid risk factors list."""
        return [
            RiskFactor(
                category="technical",
                description="API dependency",
                severity="high",
                mitigation="Build fallback"
            )
        ]

    @pytest.fixture
    def valid_gtm_strategy(self):
        """Fixture for valid GTMStrategy."""
        return GTMStrategy(
            primary_channel="Product-led",
            secondary_channels=["SEO"],
            pricing_model="Freemium",
            target_icp="SMB companies",
            time_to_first_revenue_months=3
        )

    def test_research_result_valid_complete(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult instantiation with all fields populated."""
        result = ResearchResult(
            idea_id="idea_123",
            executive_summary="This is a viable product with strong market potential.",
            market_analysis="The market is growing at 15% annually.",
            strategic_advice="Focus on SMB segment first.",
            key_assumptions=["Assumption 1", "Assumption 2"],
            recommended_next_steps=["Build MVP", "Talk to customers"],
            feasibility_score=75,
            confidence_level="high",
            investment_readiness="mvp_ready",
            market_sizing=valid_market_sizing,
            competitive_analysis=valid_competitive_analysis,
            swot_analysis=valid_swot_analysis,
            risk_factors=valid_risk_factors,
            gtm_strategy=valid_gtm_strategy,
            agent_thoughts=[
                AgentThought(
                    agent_name="Strategist",
                    thought="Strategic direction defined"
                )
            ]
        )

        assert result.idea_id == "idea_123"
        assert result.executive_summary == "This is a viable product with strong market potential."
        assert result.feasibility_score == 75
        assert result.confidence_level == "high"
        assert result.investment_readiness == "mvp_ready"
        assert result.market_sizing.tam_usd_billion == 100.0
        assert len(result.competitive_analysis.direct_competitors) == 1
        assert len(result.swot_analysis.strengths) == 1
        assert len(result.risk_factors) == 1
        assert result.gtm_strategy.primary_channel == "Product-led"
        assert len(result.agent_thoughts) == 1
        assert result.id is not None
        assert result.created_at is not None

    def test_research_result_feasibility_score_boundaries(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult accepts feasibility_score at boundaries 0-100."""
        for score in [0, 50, 100]:
            result = ResearchResult(
                idea_id="idea_123",
                executive_summary="Summary",
                market_analysis="Analysis",
                strategic_advice="Advice",
                key_assumptions=["Assumption"],
                recommended_next_steps=["Step"],
                feasibility_score=score,
                confidence_level="medium",
                investment_readiness="idea_stage",
                market_sizing=valid_market_sizing,
                competitive_analysis=valid_competitive_analysis,
                swot_analysis=valid_swot_analysis,
                risk_factors=valid_risk_factors,
                gtm_strategy=valid_gtm_strategy
            )
            assert result.feasibility_score == score

    def test_research_result_feasibility_score_out_of_range(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult raises error for feasibility_score outside 0-100."""
        with pytest.raises(ValidationError) as exc_info:
            ResearchResult(
                idea_id="idea_123",
                executive_summary="Summary",
                market_analysis="Analysis",
                strategic_advice="Advice",
                key_assumptions=["Assumption"],
                recommended_next_steps=["Step"],
                feasibility_score=150,
                confidence_level="medium",
                investment_readiness="idea_stage",
                market_sizing=valid_market_sizing,
                competitive_analysis=valid_competitive_analysis,
                swot_analysis=valid_swot_analysis,
                risk_factors=valid_risk_factors,
                gtm_strategy=valid_gtm_strategy
            )

        assert "feasibility_score" in str(exc_info.value)

    def test_research_result_valid_confidence_levels(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult accepts all valid confidence levels."""
        for level in ["low", "medium", "high"]:
            result = ResearchResult(
                idea_id="idea_123",
                executive_summary="Summary",
                market_analysis="Analysis",
                strategic_advice="Advice",
                key_assumptions=["Assumption"],
                recommended_next_steps=["Step"],
                feasibility_score=70,
                confidence_level=level,
                investment_readiness="idea_stage",
                market_sizing=valid_market_sizing,
                competitive_analysis=valid_competitive_analysis,
                swot_analysis=valid_swot_analysis,
                risk_factors=valid_risk_factors,
                gtm_strategy=valid_gtm_strategy
            )
            assert result.confidence_level == level

    def test_research_result_valid_investment_readiness_levels(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult accepts all valid investment readiness levels."""
        levels = ["pre_idea", "idea_stage", "mvp_ready", "seed_ready", "series_a_ready"]

        for level in levels:
            result = ResearchResult(
                idea_id="idea_123",
                executive_summary="Summary",
                market_analysis="Analysis",
                strategic_advice="Advice",
                key_assumptions=["Assumption"],
                recommended_next_steps=["Step"],
                feasibility_score=70,
                confidence_level="medium",
                investment_readiness=level,
                market_sizing=valid_market_sizing,
                competitive_analysis=valid_competitive_analysis,
                swot_analysis=valid_swot_analysis,
                risk_factors=valid_risk_factors,
                gtm_strategy=valid_gtm_strategy
            )
            assert result.investment_readiness == level

    def test_research_result_invalid_confidence_level(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult raises error for invalid confidence level."""
        with pytest.raises(ValidationError) as exc_info:
            ResearchResult(
                idea_id="idea_123",
                executive_summary="Summary",
                market_analysis="Analysis",
                strategic_advice="Advice",
                key_assumptions=["Assumption"],
                recommended_next_steps=["Step"],
                feasibility_score=70,
                confidence_level="very_high",
                investment_readiness="idea_stage",
                market_sizing=valid_market_sizing,
                competitive_analysis=valid_competitive_analysis,
                swot_analysis=valid_swot_analysis,
                risk_factors=valid_risk_factors,
                gtm_strategy=valid_gtm_strategy
            )

        assert "confidence_level" in str(exc_info.value)

    def test_research_result_empty_agent_thoughts(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult defaults to empty agent_thoughts list."""
        result = ResearchResult(
            idea_id="idea_123",
            executive_summary="Summary",
            market_analysis="Analysis",
            strategic_advice="Advice",
            key_assumptions=["Assumption"],
            recommended_next_steps=["Step"],
            feasibility_score=70,
            confidence_level="medium",
            investment_readiness="idea_stage",
            market_sizing=valid_market_sizing,
            competitive_analysis=valid_competitive_analysis,
            swot_analysis=valid_swot_analysis,
            risk_factors=valid_risk_factors,
            gtm_strategy=valid_gtm_strategy
        )

        assert result.agent_thoughts == []

    def test_research_result_auto_generated_id_and_timestamp(
        self,
        valid_market_sizing,
        valid_competitive_analysis,
        valid_swot_analysis,
        valid_risk_factors,
        valid_gtm_strategy
    ):
        """Test ResearchResult auto-generates ID and created_at timestamp."""
        result = ResearchResult(
            idea_id="idea_123",
            executive_summary="Summary",
            market_analysis="Analysis",
            strategic_advice="Advice",
            key_assumptions=["Assumption"],
            recommended_next_steps=["Step"],
            feasibility_score=70,
            confidence_level="medium",
            investment_readiness="idea_stage",
            market_sizing=valid_market_sizing,
            competitive_analysis=valid_competitive_analysis,
            swot_analysis=valid_swot_analysis,
            risk_factors=valid_risk_factors,
            gtm_strategy=valid_gtm_strategy
        )

        assert result.id is not None
        assert isinstance(result.id, str)
        assert len(result.id) > 0
        assert isinstance(result.created_at, datetime)
