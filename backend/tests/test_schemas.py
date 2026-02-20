# ABOUTME: Unit tests for web layer DTOs and schemas in the pipeline-enhancement feature.
# ABOUTME: Tests Pydantic validation, serialization, and deserialization for ResearchResponse and sub-schemas.

import pytest
from datetime import datetime
from pydantic import ValidationError
from src.infrastructure.web.dtos.schemas import (
    ResearchRequest,
    ResearchResponse,
    MarketSizingSchema,
    CompetitorSchema,
    CompetitiveAnalysisSchema,
    SWOTAnalysisSchema,
    RiskFactorSchema,
    GTMStrategySchema,
    AgentThoughtSchema
)


class TestResearchRequest:
    """Test suite for ResearchRequest DTO."""

    def test_research_request_valid_with_audience(self):
        """Test ResearchRequest with content and target_audience."""
        request = ResearchRequest(
            content="AI-powered task manager",
            target_audience="Remote workers"
        )

        assert request.content == "AI-powered task manager"
        assert request.target_audience == "Remote workers"

    def test_research_request_default_target_audience(self):
        """Test ResearchRequest defaults target_audience to 'General Public'."""
        request = ResearchRequest(
            content="Smart home security system"
        )

        assert request.content == "Smart home security system"
        assert request.target_audience == "General Public"

    def test_research_request_missing_content(self):
        """Test ResearchRequest raises error when content is missing."""
        with pytest.raises(ValidationError) as exc_info:
            ResearchRequest()

        assert "content" in str(exc_info.value)


class TestMarketSizingSchema:
    """Test suite for MarketSizingSchema DTO."""

    def test_market_sizing_schema_valid_complete(self):
        """Test MarketSizingSchema with all fields including optional growth_rate_pct."""
        schema = MarketSizingSchema(
            tam_usd_billion=100.5,
            sam_usd_billion=25.2,
            som_usd_million=500.0,
            sizing_methodology="hybrid",
            tam_source_basis="Gartner and internal analysis",
            growth_rate_pct=12.5
        )

        assert schema.tam_usd_billion == 100.5
        assert schema.sam_usd_billion == 25.2
        assert schema.som_usd_million == 500.0
        assert schema.sizing_methodology == "hybrid"
        assert schema.tam_source_basis == "Gartner and internal analysis"
        assert schema.growth_rate_pct == 12.5

    def test_market_sizing_schema_without_growth_rate(self):
        """Test MarketSizingSchema without optional growth_rate_pct."""
        schema = MarketSizingSchema(
            tam_usd_billion=50.0,
            sam_usd_billion=10.0,
            som_usd_million=200.0,
            sizing_methodology="top_down",
            tam_source_basis="Industry report"
        )

        assert schema.growth_rate_pct is None

    def test_market_sizing_schema_serialization(self):
        """Test MarketSizingSchema serializes to dict correctly."""
        schema = MarketSizingSchema(
            tam_usd_billion=100.0,
            sam_usd_billion=25.0,
            som_usd_million=500.0,
            sizing_methodology="bottom_up",
            tam_source_basis="Unit economics"
        )

        data = schema.model_dump()

        assert data["tam_usd_billion"] == 100.0
        assert data["sam_usd_billion"] == 25.0
        assert data["som_usd_million"] == 500.0
        assert data["sizing_methodology"] == "bottom_up"
        assert data["tam_source_basis"] == "Unit economics"


class TestCompetitorSchema:
    """Test suite for CompetitorSchema DTO."""

    def test_competitor_schema_valid_with_funding(self):
        """Test CompetitorSchema with all fields including funding."""
        schema = CompetitorSchema(
            name="CompanyX",
            positioning="AI-first platform",
            primary_weakness="Enterprise-only, no SMB offering",
            estimated_funding_usd_million=120.5,
            business_model="B2B SaaS"
        )

        assert schema.name == "CompanyX"
        assert schema.positioning == "AI-first platform"
        assert schema.primary_weakness == "Enterprise-only, no SMB offering"
        assert schema.estimated_funding_usd_million == 120.5
        assert schema.business_model == "B2B SaaS"

    def test_competitor_schema_without_funding(self):
        """Test CompetitorSchema without optional funding field."""
        schema = CompetitorSchema(
            name="StartupY",
            positioning="Freemium tool",
            primary_weakness="Limited features",
            business_model="Freemium"
        )

        assert schema.estimated_funding_usd_million is None


class TestCompetitiveAnalysisSchema:
    """Test suite for CompetitiveAnalysisSchema DTO."""

    def test_competitive_analysis_schema_valid(self):
        """Test CompetitiveAnalysisSchema with competitor lists."""
        schema = CompetitiveAnalysisSchema(
            direct_competitors=[
                CompetitorSchema(
                    name="DirectComp1",
                    positioning="Same solution",
                    primary_weakness="High pricing",
                    business_model="Enterprise SaaS"
                )
            ],
            indirect_competitors=[
                CompetitorSchema(
                    name="IndirectComp1",
                    positioning="Different approach",
                    primary_weakness="Manual process",
                    business_model="Consulting"
                )
            ],
            competitive_moat="Proprietary data and network effects",
            differentiation_score=9
        )

        assert len(schema.direct_competitors) == 1
        assert len(schema.indirect_competitors) == 1
        assert schema.competitive_moat == "Proprietary data and network effects"
        assert schema.differentiation_score == 9

    def test_competitive_analysis_schema_serialization(self):
        """Test CompetitiveAnalysisSchema serializes nested competitors correctly."""
        schema = CompetitiveAnalysisSchema(
            direct_competitors=[
                CompetitorSchema(
                    name="Comp1",
                    positioning="Position",
                    primary_weakness="Weakness",
                    business_model="SaaS"
                )
            ],
            indirect_competitors=[],
            competitive_moat="Tech moat",
            differentiation_score=7
        )

        data = schema.model_dump()

        assert len(data["direct_competitors"]) == 1
        assert data["direct_competitors"][0]["name"] == "Comp1"
        assert len(data["indirect_competitors"]) == 0


class TestSWOTAnalysisSchema:
    """Test suite for SWOTAnalysisSchema DTO."""

    def test_swot_analysis_schema_valid(self):
        """Test SWOTAnalysisSchema with all quadrants."""
        schema = SWOTAnalysisSchema(
            strengths=["Strong team", "First mover", "Patent pending"],
            weaknesses=["Limited funding", "No sales team"],
            opportunities=["Market growth", "New regulation"],
            threats=["Competitive pressure", "Economic downturn"]
        )

        assert len(schema.strengths) == 3
        assert len(schema.weaknesses) == 2
        assert len(schema.opportunities) == 2
        assert len(schema.threats) == 2

    def test_swot_analysis_schema_empty_quadrants(self):
        """Test SWOTAnalysisSchema allows empty lists."""
        schema = SWOTAnalysisSchema(
            strengths=["Only strength"],
            weaknesses=[],
            opportunities=[],
            threats=[]
        )

        assert len(schema.strengths) == 1
        assert len(schema.weaknesses) == 0


class TestRiskFactorSchema:
    """Test suite for RiskFactorSchema DTO."""

    def test_risk_factor_schema_valid_all_categories(self):
        """Test RiskFactorSchema with all valid categories."""
        categories = ["market", "technical", "regulatory", "competitive", "financial", "execution"]

        for category in categories:
            schema = RiskFactorSchema(
                category=category,
                description="Risk description",
                severity="medium",
                mitigation="Mitigation plan"
            )
            assert schema.category == category

    def test_risk_factor_schema_valid_all_severities(self):
        """Test RiskFactorSchema with all valid severities."""
        severities = ["low", "medium", "high", "critical"]

        for severity in severities:
            schema = RiskFactorSchema(
                category="technical",
                description="Risk description",
                severity=severity,
                mitigation="Mitigation plan"
            )
            assert schema.severity == severity

    def test_risk_factor_schema_serialization(self):
        """Test RiskFactorSchema serializes to dict correctly."""
        schema = RiskFactorSchema(
            category="regulatory",
            description="GDPR compliance required",
            severity="high",
            mitigation="Hire compliance consultant"
        )

        data = schema.model_dump()

        assert data["category"] == "regulatory"
        assert data["description"] == "GDPR compliance required"
        assert data["severity"] == "high"
        assert data["mitigation"] == "Hire compliance consultant"


class TestGTMStrategySchema:
    """Test suite for GTMStrategySchema DTO."""

    def test_gtm_strategy_schema_valid_with_cac(self):
        """Test GTMStrategySchema with all fields including CAC."""
        schema = GTMStrategySchema(
            primary_channel="Product-led growth",
            secondary_channels=["SEO", "Content marketing", "Partnerships"],
            pricing_model="Freemium ($0 free, $99/mo Pro)",
            estimated_cac_usd=500.0,
            target_icp="Series A SaaS companies with 20-100 employees",
            time_to_first_revenue_months=4
        )

        assert schema.primary_channel == "Product-led growth"
        assert len(schema.secondary_channels) == 3
        assert schema.pricing_model == "Freemium ($0 free, $99/mo Pro)"
        assert schema.estimated_cac_usd == 500.0
        assert "Series A SaaS" in schema.target_icp
        assert schema.time_to_first_revenue_months == 4

    def test_gtm_strategy_schema_without_cac(self):
        """Test GTMStrategySchema without optional CAC."""
        schema = GTMStrategySchema(
            primary_channel="Enterprise sales",
            secondary_channels=["Events"],
            pricing_model="Annual contract",
            target_icp="Fortune 500 companies",
            time_to_first_revenue_months=12
        )

        assert schema.estimated_cac_usd is None


class TestAgentThoughtSchema:
    """Test suite for AgentThoughtSchema DTO."""

    def test_agent_thought_schema_valid(self):
        """Test AgentThoughtSchema with all fields."""
        timestamp = datetime.utcnow()
        schema = AgentThoughtSchema(
            agent_name="Market Analyst",
            thought="Conducted comprehensive market research",
            timestamp=timestamp
        )

        assert schema.agent_name == "Market Analyst"
        assert schema.thought == "Conducted comprehensive market research"
        assert schema.timestamp == timestamp

    def test_agent_thought_schema_serialization(self):
        """Test AgentThoughtSchema serializes timestamp correctly."""
        timestamp = datetime.utcnow()
        schema = AgentThoughtSchema(
            agent_name="Strategist",
            thought="Strategic direction defined",
            timestamp=timestamp
        )

        data = schema.model_dump()

        assert data["agent_name"] == "Strategist"
        assert data["thought"] == "Strategic direction defined"
        assert isinstance(data["timestamp"], datetime)


class TestResearchResponse:
    """Test suite for ResearchResponse DTO."""

    @pytest.fixture
    def complete_response_data(self):
        """Fixture providing complete ResearchResponse data."""
        return {
            "id": "result_123",
            "idea_id": "idea_456",
            "executive_summary": "This product has strong market potential with clear differentiation.",
            "market_analysis": "The market is growing at 15% annually with strong tailwinds.",
            "strategic_advice": "Focus on SMB segment first, then expand to enterprise.",
            "key_assumptions": ["Assumption 1: Market growth continues", "Assumption 2: Tech adoption accelerates"],
            "recommended_next_steps": ["Build MVP", "Interview 20 customers", "Validate pricing"],
            "feasibility_score": 78,
            "confidence_level": "high",
            "investment_readiness": "seed_ready",
            "market_sizing": {
                "tam_usd_billion": 100.0,
                "sam_usd_billion": 25.0,
                "som_usd_million": 500.0,
                "sizing_methodology": "hybrid",
                "tam_source_basis": "Gartner + internal analysis"
            },
            "competitive_analysis": {
                "direct_competitors": [
                    {
                        "name": "CompetitorX",
                        "positioning": "Enterprise platform",
                        "primary_weakness": "Complex onboarding",
                        "business_model": "B2B SaaS"
                    }
                ],
                "indirect_competitors": [],
                "competitive_moat": "Network effects",
                "differentiation_score": 8
            },
            "swot_analysis": {
                "strengths": ["Strong team", "First mover"],
                "weaknesses": ["Limited funding"],
                "opportunities": ["Market growth"],
                "threats": ["Competition"]
            },
            "risk_factors": [
                {
                    "category": "technical",
                    "description": "API dependency",
                    "severity": "high",
                    "mitigation": "Build fallback"
                }
            ],
            "gtm_strategy": {
                "primary_channel": "Product-led",
                "secondary_channels": ["SEO"],
                "pricing_model": "Freemium",
                "target_icp": "SMB SaaS companies",
                "time_to_first_revenue_months": 3
            },
            "agent_thoughts": [
                {
                    "agent_name": "Strategist",
                    "thought": "Strategic direction defined",
                    "timestamp": datetime.utcnow()
                }
            ]
        }

    def test_research_response_valid_complete(self, complete_response_data):
        """Test ResearchResponse instantiation with all fields."""
        response = ResearchResponse(**complete_response_data)

        assert response.id == "result_123"
        assert response.idea_id == "idea_456"
        assert response.executive_summary == complete_response_data["executive_summary"]
        assert response.market_analysis == complete_response_data["market_analysis"]
        assert response.strategic_advice == complete_response_data["strategic_advice"]
        assert len(response.key_assumptions) == 2
        assert len(response.recommended_next_steps) == 3
        assert response.feasibility_score == 78
        assert response.confidence_level == "high"
        assert response.investment_readiness == "seed_ready"

    def test_research_response_nested_market_sizing(self, complete_response_data):
        """Test ResearchResponse correctly parses nested MarketSizingSchema."""
        response = ResearchResponse(**complete_response_data)

        assert isinstance(response.market_sizing, MarketSizingSchema)
        assert response.market_sizing.tam_usd_billion == 100.0
        assert response.market_sizing.sam_usd_billion == 25.0
        assert response.market_sizing.som_usd_million == 500.0
        assert response.market_sizing.sizing_methodology == "hybrid"

    def test_research_response_nested_competitive_analysis(self, complete_response_data):
        """Test ResearchResponse correctly parses nested CompetitiveAnalysisSchema."""
        response = ResearchResponse(**complete_response_data)

        assert isinstance(response.competitive_analysis, CompetitiveAnalysisSchema)
        assert len(response.competitive_analysis.direct_competitors) == 1
        assert isinstance(response.competitive_analysis.direct_competitors[0], CompetitorSchema)
        assert response.competitive_analysis.direct_competitors[0].name == "CompetitorX"
        assert response.competitive_analysis.differentiation_score == 8

    def test_research_response_nested_swot_analysis(self, complete_response_data):
        """Test ResearchResponse correctly parses nested SWOTAnalysisSchema."""
        response = ResearchResponse(**complete_response_data)

        assert isinstance(response.swot_analysis, SWOTAnalysisSchema)
        assert len(response.swot_analysis.strengths) == 2
        assert len(response.swot_analysis.weaknesses) == 1
        assert "Strong team" in response.swot_analysis.strengths

    def test_research_response_nested_risk_factors(self, complete_response_data):
        """Test ResearchResponse correctly parses list of RiskFactorSchema."""
        response = ResearchResponse(**complete_response_data)

        assert isinstance(response.risk_factors, list)
        assert len(response.risk_factors) == 1
        assert isinstance(response.risk_factors[0], RiskFactorSchema)
        assert response.risk_factors[0].category == "technical"
        assert response.risk_factors[0].severity == "high"

    def test_research_response_nested_gtm_strategy(self, complete_response_data):
        """Test ResearchResponse correctly parses nested GTMStrategySchema."""
        response = ResearchResponse(**complete_response_data)

        assert isinstance(response.gtm_strategy, GTMStrategySchema)
        assert response.gtm_strategy.primary_channel == "Product-led"
        assert len(response.gtm_strategy.secondary_channels) == 1
        assert response.gtm_strategy.time_to_first_revenue_months == 3

    def test_research_response_nested_agent_thoughts(self, complete_response_data):
        """Test ResearchResponse correctly parses list of AgentThoughtSchema."""
        response = ResearchResponse(**complete_response_data)

        assert isinstance(response.agent_thoughts, list)
        assert len(response.agent_thoughts) == 1
        assert isinstance(response.agent_thoughts[0], AgentThoughtSchema)
        assert response.agent_thoughts[0].agent_name == "Strategist"

    def test_research_response_empty_agent_thoughts(self, complete_response_data):
        """Test ResearchResponse allows empty agent_thoughts list."""
        complete_response_data["agent_thoughts"] = []
        response = ResearchResponse(**complete_response_data)

        assert response.agent_thoughts == []

    def test_research_response_serialization(self, complete_response_data):
        """Test ResearchResponse serializes to dict with all nested schemas."""
        response = ResearchResponse(**complete_response_data)
        data = response.model_dump()

        # Verify top-level fields
        assert data["id"] == "result_123"
        assert data["idea_id"] == "idea_456"
        assert data["feasibility_score"] == 78

        # Verify nested schemas serialized
        assert isinstance(data["market_sizing"], dict)
        assert data["market_sizing"]["tam_usd_billion"] == 100.0

        assert isinstance(data["competitive_analysis"], dict)
        assert isinstance(data["competitive_analysis"]["direct_competitors"], list)

        assert isinstance(data["swot_analysis"], dict)
        assert isinstance(data["swot_analysis"]["strengths"], list)

        assert isinstance(data["risk_factors"], list)
        assert isinstance(data["gtm_strategy"], dict)
        assert isinstance(data["agent_thoughts"], list)

    def test_research_response_json_serialization(self, complete_response_data):
        """Test ResearchResponse can be serialized to JSON."""
        response = ResearchResponse(**complete_response_data)
        json_str = response.model_dump_json()

        assert isinstance(json_str, str)
        assert "result_123" in json_str
        assert "executive_summary" in json_str
        assert "market_sizing" in json_str

    def test_research_response_deserialization_from_json(self, complete_response_data):
        """Test ResearchResponse can be deserialized from JSON."""
        response = ResearchResponse(**complete_response_data)
        json_str = response.model_dump_json()

        # Deserialize back
        deserialized = ResearchResponse.model_validate_json(json_str)

        assert deserialized.id == response.id
        assert deserialized.executive_summary == response.executive_summary
        assert deserialized.market_sizing.tam_usd_billion == response.market_sizing.tam_usd_billion

    def test_research_response_invalid_confidence_level(self, complete_response_data):
        """Test ResearchResponse raises error for invalid confidence_level."""
        complete_response_data["confidence_level"] = "super_high"

        with pytest.raises(ValidationError) as exc_info:
            ResearchResponse(**complete_response_data)

        assert "confidence_level" in str(exc_info.value)

    def test_research_response_invalid_investment_readiness(self, complete_response_data):
        """Test ResearchResponse raises error for invalid investment_readiness."""
        complete_response_data["investment_readiness"] = "unicorn_ready"

        with pytest.raises(ValidationError) as exc_info:
            ResearchResponse(**complete_response_data)

        assert "investment_readiness" in str(exc_info.value)

    def test_research_response_missing_required_nested_field(self, complete_response_data):
        """Test ResearchResponse raises error when required nested field is missing."""
        # Remove required field from market_sizing
        del complete_response_data["market_sizing"]["sizing_methodology"]

        with pytest.raises(ValidationError) as exc_info:
            ResearchResponse(**complete_response_data)

        assert "sizing_methodology" in str(exc_info.value)
