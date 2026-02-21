# ABOUTME: Unit and integration tests for PydanticAgentAdapter
# ABOUTME: Validates SWOT agent configuration, schema validation, and output structure

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from pydantic import ValidationError
from src.infrastructure.adapters.agent_adapter import PydanticAgentAdapter, SWOTRiskOutput
from src.domain.entities import SWOTAnalysis, RiskFactor
from src.config.settings import settings


class TestSWOTAgentConfiguration:
    """Unit tests for SWOT agent configuration"""

    @patch('src.infrastructure.adapters.agent_adapter.Agent')
    def test_swot_agent_uses_correct_model(self, mock_agent_class):
        """Verify SWOT agent is initialized with LLM_MODEL (Gemini 3 Flash Preview)"""
        adapter = PydanticAgentAdapter()

        # Find the call that initialized swot_risk_agent
        calls = mock_agent_class.call_args_list
        swot_call = None
        for call in calls:
            if call.kwargs.get('output_type') == SWOTRiskOutput:
                swot_call = call
                break

        assert swot_call is not None, "SWOT agent was not initialized"
        assert swot_call.args[0] == settings.LLM_MODEL, \
            f"SWOT agent should use LLM_MODEL, got {swot_call.args[0]}"

    @patch('src.infrastructure.adapters.agent_adapter.Agent')
    def test_swot_agent_uses_correct_temperature(self, mock_agent_class):
        """Verify SWOT agent uses temperature 0.2 for structured output consistency"""
        adapter = PydanticAgentAdapter()

        # Find the call that initialized swot_risk_agent
        calls = mock_agent_class.call_args_list
        swot_call = None
        for call in calls:
            if call.kwargs.get('output_type') == SWOTRiskOutput:
                swot_call = call
                break

        assert swot_call is not None, "SWOT agent was not initialized"
        model_settings = swot_call.kwargs.get('model_settings')
        assert model_settings is not None, "SWOT agent should have model_settings"
        # ModelSettings is passed as a dict when mocked
        if isinstance(model_settings, dict):
            assert model_settings.get('temperature') == 0.2, \
                f"SWOT agent should use temperature 0.2, got {model_settings.get('temperature')}"
        else:
            # ModelSettings object
            assert hasattr(model_settings, 'temperature'), "model_settings should have temperature attribute"
            assert model_settings.temperature == 0.2, \
                f"SWOT agent should use temperature 0.2, got {model_settings.temperature}"

    @patch('src.infrastructure.adapters.agent_adapter.Agent')
    def test_swot_agent_has_retries(self, mock_agent_class):
        """Verify SWOT agent is configured with 5 retries"""
        adapter = PydanticAgentAdapter()

        # Find the call that initialized swot_risk_agent
        calls = mock_agent_class.call_args_list
        swot_call = None
        for call in calls:
            if call.kwargs.get('output_type') == SWOTRiskOutput:
                swot_call = call
                break

        assert swot_call is not None, "SWOT agent was not initialized"
        assert swot_call.kwargs.get('retries') == 5, \
            f"SWOT agent should have 5 retries, got {swot_call.kwargs.get('retries')}"

    @patch('src.infrastructure.adapters.agent_adapter.Agent')
    def test_gtm_agent_uses_correct_model(self, mock_agent_class):
        """Verify GTM agent also uses LLM_MODEL (same model as SWOT)"""
        from src.domain.entities import GTMStrategy
        adapter = PydanticAgentAdapter()

        # Find the call that initialized gtm_agent
        calls = mock_agent_class.call_args_list
        gtm_call = None
        for call in calls:
            if call.kwargs.get('output_type') == GTMStrategy:
                gtm_call = call
                break

        assert gtm_call is not None, "GTM agent was not initialized"
        assert gtm_call.args[0] == settings.LLM_MODEL, \
            f"GTM agent should use LLM_MODEL, got {gtm_call.args[0]}"


class TestSWOTRiskOutputSchema:
    """Schema validation tests for SWOTRiskOutput"""

    def test_valid_swot_risk_output(self):
        """Test that valid SWOTRiskOutput with flattened fields passes validation"""
        valid_data = {
            "strengths": ["Strong team", "Unique tech", "Market timing"],
            "weaknesses": ["No funding", "Small team", "Limited reach"],
            "opportunities": ["Growing market", "New regulation", "Tech trends"],
            "threats": ["Competition", "Economic downturn", "Tech changes"],
            "risk_categories": ["market", "technical", "financial", "execution"],
            "risk_descriptions": [
                "Market may not adopt the product quickly enough",
                "Core technology may not scale as expected",
                "Funding may run out before profitability",
                "Team may not execute quickly enough"
            ],
            "risk_severities": ["critical", "high", "medium", "low"],
            "risk_mitigations": [
                "Conduct extensive user research and pilot programs",
                "Build scalable architecture from day one",
                "Maintain 18-month runway, plan fundraising early",
                "Hire experienced team members, use agile methodology"
            ]
        }

        output = SWOTRiskOutput(**valid_data)
        assert output.strengths == valid_data["strengths"]
        assert output.weaknesses == valid_data["weaknesses"]
        assert len(output.risk_categories) == 4
        assert output.risk_categories[0] == "market"
        assert output.risk_severities[0] == "critical"

    def test_swot_with_minimum_items(self):
        """Test SWOT with minimum 3 items per quadrant and 4 risks (edge case)"""
        min_data = {
            "strengths": ["S1", "S2", "S3"],
            "weaknesses": ["W1", "W2", "W3"],
            "opportunities": ["O1", "O2", "O3"],
            "threats": ["T1", "T2", "T3"],
            "risk_categories": ["market", "technical", "financial", "execution"],
            "risk_descriptions": ["R1", "R2", "R3", "R4"],
            "risk_severities": ["high", "medium", "low", "critical"],
            "risk_mitigations": ["M1", "M2", "M3", "M4"]
        }

        output = SWOTRiskOutput(**min_data)
        assert len(output.strengths) == 3
        assert len(output.risk_categories) == 4

    def test_swot_with_maximum_items(self):
        """Test SWOT with maximum 5 items per quadrant and 7 risks (edge case)"""
        max_data = {
            "strengths": ["S1", "S2", "S3", "S4", "S5"],
            "weaknesses": ["W1", "W2", "W3", "W4", "W5"],
            "opportunities": ["O1", "O2", "O3", "O4", "O5"],
            "threats": ["T1", "T2", "T3", "T4", "T5"],
            "risk_categories": ["market", "technical", "regulatory", "competitive", "financial", "execution", "market"],
            "risk_descriptions": ["R1", "R2", "R3", "R4", "R5", "R6", "R7"],
            "risk_severities": ["critical", "critical", "high", "high", "medium", "medium", "low"],
            "risk_mitigations": ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
        }

        output = SWOTRiskOutput(**max_data)
        assert len(output.strengths) == 5
        assert len(output.risk_categories) == 7

    def test_invalid_risk_category(self):
        """Test that invalid risk category fails validation"""
        invalid_data = {
            "strengths": ["S1", "S2", "S3"],
            "weaknesses": ["W1", "W2", "W3"],
            "opportunities": ["O1", "O2", "O3"],
            "threats": ["T1", "T2", "T3"],
            "risk_categories": ["invalid_category", "market", "technical", "financial"],  # First one invalid
            "risk_descriptions": ["R1", "R2", "R3", "R4"],
            "risk_severities": ["high", "medium", "low", "critical"],
            "risk_mitigations": ["M1", "M2", "M3", "M4"]
        }

        with pytest.raises(ValidationError) as exc_info:
            SWOTRiskOutput(**invalid_data)

        assert "risk_categories" in str(exc_info.value)

    def test_invalid_risk_severity(self):
        """Test that invalid risk severity fails validation"""
        invalid_data = {
            "strengths": ["S1", "S2", "S3"],
            "weaknesses": ["W1", "W2", "W3"],
            "opportunities": ["O1", "O2", "O3"],
            "threats": ["T1", "T2", "T3"],
            "risk_categories": ["market", "technical", "financial", "execution"],
            "risk_descriptions": ["R1", "R2", "R3", "R4"],
            "risk_severities": ["extreme", "high", "medium", "low"],  # First one invalid
            "risk_mitigations": ["M1", "M2", "M3", "M4"]
        }

        with pytest.raises(ValidationError) as exc_info:
            SWOTRiskOutput(**invalid_data)

        assert "risk_severities" in str(exc_info.value)

    def test_empty_swot_quadrant_fails(self):
        """Test that empty SWOT quadrant fails validation with min_length=3"""
        invalid_data = {
            "strengths": [],  # Empty - should fail min_length=3
            "weaknesses": ["W1", "W2", "W3"],
            "opportunities": ["O1", "O2", "O3"],
            "threats": ["T1", "T2", "T3"],
            "risk_categories": ["market", "technical", "financial", "execution"],
            "risk_descriptions": ["R1", "R2", "R3", "R4"],
            "risk_severities": ["high", "medium", "low", "critical"],
            "risk_mitigations": ["M1", "M2", "M3", "M4"]
        }

        with pytest.raises(ValidationError) as exc_info:
            SWOTRiskOutput(**invalid_data)

        assert "strengths" in str(exc_info.value)

    def test_missing_risk_field_fails(self):
        """Test that missing required risk field fails validation"""
        invalid_data = {
            "swot": {
                "strengths": ["S1", "S2", "S3"],
                "weaknesses": ["W1", "W2", "W3"],
                "opportunities": ["O1", "O2", "O3"],
                "threats": ["T1", "T2", "T3"]
            },
            "risks": [
                {
                    "category": "market",
                    "description": "Risk description",
                    "severity": "high"
                    # Missing mitigation field
                },
                {
                    "category": "technical",
                    "description": "Risk 2",
                    "severity": "medium",
                    "mitigation": "Mitigation 2"
                },
                {
                    "category": "financial",
                    "description": "Risk 3",
                    "severity": "low",
                    "mitigation": "Mitigation 3"
                },
                {
                    "category": "execution",
                    "description": "Risk 4",
                    "severity": "critical",
                    "mitigation": "Mitigation 4"
                }
            ]
        }

        with pytest.raises(ValidationError) as exc_info:
            SWOTRiskOutput(**invalid_data)

        assert "mitigation" in str(exc_info.value)


class TestSWOTAgentBehavior:
    """Integration tests for SWOT agent behavior with mocked LLM responses"""

    @pytest.mark.asyncio
    async def test_swot_agent_returns_all_quadrants_populated(self):
        """Test that SWOT agent returns all 4 quadrants with 3-5 items each"""
        adapter = PydanticAgentAdapter()

        # Mock the agent's run method to return flattened output
        mock_result = MagicMock()
        mock_result.output = SWOTRiskOutput(
            strengths=["Strength 1", "Strength 2", "Strength 3", "Strength 4"],
            weaknesses=["Weakness 1", "Weakness 2", "Weakness 3"],
            opportunities=["Opportunity 1", "Opportunity 2", "Opportunity 3", "Opportunity 4"],
            threats=["Threat 1", "Threat 2", "Threat 3"],
            risk_categories=["market", "technical", "financial", "execution"],
            risk_descriptions=["Market risk", "Tech risk", "Financial risk", "Execution risk"],
            risk_severities=["critical", "high", "medium", "low"],
            risk_mitigations=["Mitigation 1", "Mitigation 2", "Mitigation 3", "Mitigation 4"]
        )

        adapter.swot_risk_agent.run = AsyncMock(return_value=mock_result)

        result = await adapter.analyze_swot_risks(
            "AI-powered dental practice automation",
            "Strategic input from previous agent"
        )

        # Verify all quadrants are populated (converted back to nested structure)
        assert len(result["swot"].strengths) >= 3
        assert len(result["swot"].weaknesses) >= 3
        assert len(result["swot"].opportunities) >= 3
        assert len(result["swot"].threats) >= 3

    @pytest.mark.asyncio
    async def test_swot_agent_returns_valid_risk_count(self):
        """Test that SWOT agent returns 4-7 risks"""
        adapter = PydanticAgentAdapter()

        mock_result = MagicMock()
        mock_result.output = SWOTRiskOutput(
            strengths=["S1", "S2", "S3", "S4"],
            weaknesses=["W1", "W2", "W3"],
            opportunities=["O1", "O2", "O3", "O4"],
            threats=["T1", "T2", "T3"],
            risk_categories=["market", "technical", "regulatory", "competitive", "financial", "execution"],
            risk_descriptions=["R1", "R2", "R3", "R4", "R5", "R6"],
            risk_severities=["critical", "critical", "high", "high", "medium", "low"],
            risk_mitigations=["M1", "M2", "M3", "M4", "M5", "M6"]
        )

        adapter.swot_risk_agent.run = AsyncMock(return_value=mock_result)

        result = await adapter.analyze_swot_risks(
            "Blockchain-based supply chain tracking",
            "Strategic input"
        )

        assert 4 <= len(result["risks"]) <= 7

    @pytest.mark.asyncio
    async def test_swot_agent_validates_risk_categories(self):
        """Test that all risk categories are valid Literals"""
        adapter = PydanticAgentAdapter()

        valid_categories = ["market", "technical", "regulatory", "competitive", "financial", "execution"]

        mock_result = MagicMock()
        mock_result.output = SWOTRiskOutput(
            strengths=["S1", "S2", "S3"],
            weaknesses=["W1", "W2", "W3"],
            opportunities=["O1", "O2", "O3"],
            threats=["T1", "T2", "T3"],
            risk_categories=["market", "technical", "regulatory", "financial"],
            risk_descriptions=["R1", "R2", "R3", "R4"],
            risk_severities=["high", "medium", "low", "critical"],
            risk_mitigations=["M1", "M2", "M3", "M4"]
        )

        adapter.swot_risk_agent.run = AsyncMock(return_value=mock_result)

        result = await adapter.analyze_swot_risks("Product idea", "Strategic input")

        # result["risks"] contains RiskFactor Pydantic objects
        for risk in result["risks"]:
            assert risk.category in valid_categories

    @pytest.mark.asyncio
    async def test_swot_agent_validates_risk_severities(self):
        """Test that all risk severities are valid Literals"""
        adapter = PydanticAgentAdapter()

        valid_severities = ["low", "medium", "high", "critical"]

        mock_result = MagicMock()
        mock_result.output = SWOTRiskOutput(
            strengths=["S1", "S2", "S3"],
            weaknesses=["W1", "W2", "W3"],
            opportunities=["O1", "O2", "O3"],
            threats=["T1", "T2", "T3"],
            risk_categories=["market", "technical", "financial", "execution"],
            risk_descriptions=["R1", "R2", "R3", "R4"],
            risk_severities=["critical", "high", "medium", "low"],
            risk_mitigations=["M1", "M2", "M3", "M4"]
        )

        adapter.swot_risk_agent.run = AsyncMock(return_value=mock_result)

        result = await adapter.analyze_swot_risks("Product idea", "Strategic input")

        # result["risks"] contains RiskFactor Pydantic objects
        for risk in result["risks"]:
            assert risk.severity in valid_severities
