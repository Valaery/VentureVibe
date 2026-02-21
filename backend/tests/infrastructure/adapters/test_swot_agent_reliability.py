# ABOUTME: Reliability tests for SWOT & Risk agent with real API calls
# ABOUTME: Validates <5% error rate across 20 diverse product ideas

import pytest
import asyncio
import logging
from typing import List, Dict, Any
from src.infrastructure.adapters.agent_adapter import PydanticAgentAdapter

# Configure logging
logger = logging.getLogger(__name__)


# Diverse product ideas covering multiple domains, languages, and complexity levels
DIVERSE_PRODUCT_IDEAS = [
    # 1. Spanish language input (as seen in failing trace)
    {
        "idea": "Plataforma de automatización de clínicas dentales con IA para gestión de citas y comunicación con pacientes",
        "audience": "Clínicas dentales privadas en España y Latinoamérica"
    },
    # 2. Highly technical - Blockchain
    {
        "idea": "Blockchain-based supply chain verification system for pharmaceutical companies using zero-knowledge proofs",
        "audience": "Enterprise pharmaceutical manufacturers and distributors"
    },
    # 3. Highly technical - AI/ML
    {
        "idea": "Federated learning platform for training medical AI models across hospitals without sharing patient data",
        "audience": "Healthcare systems and medical research institutions"
    },
    # 4. Highly technical - Biotech
    {
        "idea": "CRISPR gene editing workflow automation software with AI-assisted guide RNA design",
        "audience": "Biotech research labs and pharmaceutical R&D teams"
    },
    # 5. Non-technical consumer product
    {
        "idea": "Subscription box service for eco-friendly cleaning products tailored to home size and preferences",
        "audience": "Environmentally conscious homeowners aged 25-45"
    },
    # 6. Non-technical B2C
    {
        "idea": "Mobile app connecting home cooks with neighbors for meal sharing and community dining",
        "audience": "Urban professionals who enjoy cooking and community connection"
    },
    # 7. Vague/underdeveloped idea
    {
        "idea": "An app to help people be more productive",
        "audience": "Anyone who wants to get more done"
    },
    # 8. Vague B2B idea
    {
        "idea": "Software to make businesses run better using AI",
        "audience": "Small and medium businesses"
    },
    # 9. Extremely detailed product specification
    {
        "idea": """Real-time collaborative code review platform with AI-powered security vulnerability detection, integrated with GitHub/GitLab/Bitbucket.
        Features: (1) Live code review sessions with video chat, (2) ML models trained on OWASP Top 10 and CWE database detecting vulnerabilities with 92% accuracy,
        (3) Automated fix suggestions using GPT-4-based code generation, (4) Compliance reporting for SOC2/ISO27001/HIPAA,
        (5) Integration with Jira/Linear for automated ticket creation, (6) Analytics dashboard showing team velocity and security debt metrics.
        Tech stack: Python backend (FastAPI), React frontend, PostgreSQL + Redis, deployed on AWS EKS.
        Pricing: $49/dev/month for teams under 20, $39/dev/month for 20-100, enterprise pricing for 100+.""",
        "audience": "Engineering teams at Series A-C startups (20-200 engineers) in fintech, healthcare, and security-conscious industries"
    },
    # 10. Detailed hardware + software
    {
        "idea": """Smart irrigation system with soil sensors, weather API integration, and ML-based watering optimization.
        Hardware: IoT soil moisture/pH/temperature sensors (4 per zone), cellular gateway (CAT-M1), solenoid valve controllers.
        Software: Mobile app (iOS/Android) for zone configuration, cloud backend for ML predictions, integration with Weather Underground API.
        Saves 30-50% water usage vs traditional timers.""",
        "audience": "Commercial property managers (office parks, retail centers) and high-end residential landscapers in water-scarce regions (California, Arizona, Texas)"
    },
    # 11. Regulated industry - Healthcare
    {
        "idea": "HIPAA-compliant telemedicine platform specializing in pediatric mental health with parent portal and therapist dashboard",
        "audience": "Licensed child psychologists and parents of children aged 6-17"
    },
    # 12. Regulated industry - Fintech
    {
        "idea": "Embedded banking API for gig economy platforms to offer instant payouts and financial services to contractors",
        "audience": "Gig economy platform companies (rideshare, delivery, freelance marketplaces)"
    },
    # 13. Social impact / mission-driven
    {
        "idea": "Mobile learning platform teaching digital literacy and remote work skills to refugees and displaced populations",
        "audience": "NGOs, refugee resettlement agencies, and displaced individuals in refugee camps"
    },
    # 14. Climate tech
    {
        "idea": "Carbon accounting SaaS for mid-market companies to track Scope 1, 2, and 3 emissions with supplier data integration",
        "audience": "Sustainability managers at manufacturing and retail companies (500-5000 employees) preparing for ESG reporting requirements"
    },
    # 15. Deep tech / moonshot
    {
        "idea": "Quantum-resistant encryption SDK for securing IoT device communications in preparation for post-quantum cryptography era",
        "audience": "Enterprise IoT platform vendors and security-conscious device manufacturers"
    },
    # 16. Local/hyperlocal service
    {
        "idea": "On-demand laundry pickup and delivery service with eco-friendly cleaning for apartment buildings",
        "audience": "Urban apartment residents in high-density neighborhoods without in-unit laundry"
    },
    # 17. B2B SaaS - HR tech
    {
        "idea": "AI-powered interview scheduling and candidate communication platform integrated with ATS systems",
        "audience": "Recruiting teams at high-growth startups (50-500 employees) hiring 10+ people per month"
    },
    # 18. B2B SaaS - MarTech
    {
        "idea": "Automated SEO content optimization tool that rewrites existing blog posts to rank for high-value keywords",
        "audience": "Content marketing teams at B2B SaaS companies with 100+ published articles"
    },
    # 19. Marketplace / two-sided platform
    {
        "idea": "Freelance marketplace connecting certified solar panel installers with homeowners, with financing integration",
        "audience": "Homeowners interested in solar installation and independent solar installation contractors"
    },
    # 20. Gaming / entertainment
    {
        "idea": "AI dungeon master for tabletop RPG games that generates adaptive storylines based on player choices",
        "audience": "Tabletop RPG players (D&D, Pathfinder) who struggle to find consistent in-person game groups"
    }
]


class TestSWOTAgentReliability:
    """Reliability tests for SWOT agent across diverse product ideas"""

    @pytest.mark.asyncio
    @pytest.mark.slow  # Mark as slow test since it makes 20 API calls
    async def test_swot_agent_20_run_reliability(self):
        """
        Run SWOT agent 20 times with diverse product ideas.
        Target: <5% error rate (≥19 successful runs out of 20)
        """
        adapter = PydanticAgentAdapter()
        results: List[Dict[str, Any]] = []
        failures: List[Dict[str, Any]] = []

        logger.info("Starting SWOT agent reliability test with 20 diverse product ideas...")

        for idx, test_case in enumerate(DIVERSE_PRODUCT_IDEAS, 1):
            logger.info(f"\n[{idx}/20] Testing: {test_case['idea'][:100]}...")

            try:
                # Get strategic input first (simplified for testing)
                strategic_input = f"Product validation for: {test_case['idea']}"

                # Run SWOT analysis
                result = await adapter.analyze_swot_risks(
                    test_case["idea"],
                    strategic_input
                )

                # Validate result structure
                assert "swot" in result, "Result missing 'swot' field"
                assert "risks" in result, "Result missing 'risks' field"

                # Validate SWOT quadrants (result returns Pydantic objects)
                swot = result["swot"]
                assert len(swot.strengths) >= 3, \
                    f"Strengths should have ≥3 items, got {len(swot.strengths)}"
                assert len(swot.weaknesses) >= 3, \
                    f"Weaknesses should have ≥3 items, got {len(swot.weaknesses)}"
                assert len(swot.opportunities) >= 3, \
                    f"Opportunities should have ≥3 items, got {len(swot.opportunities)}"
                assert len(swot.threats) >= 3, \
                    f"Threats should have ≥3 items, got {len(swot.threats)}"

                # Validate risks (list of RiskFactor Pydantic objects)
                risks = result["risks"]
                assert 4 <= len(risks) <= 7, \
                    f"Risks should be 4-7, got {len(risks)}"

                # Validate risk fields
                valid_categories = ["market", "technical", "regulatory", "competitive", "financial", "execution"]
                valid_severities = ["low", "medium", "high", "critical"]

                for risk_idx, risk in enumerate(risks):
                    assert risk.category in valid_categories, \
                        f"Risk {risk_idx} has invalid category: {risk.category}"
                    assert risk.severity in valid_severities, \
                        f"Risk {risk_idx} has invalid severity: {risk.severity}"
                    assert len(risk.description) > 10, \
                        f"Risk {risk_idx} has insufficient description"
                    assert len(risk.mitigation) > 10, \
                        f"Risk {risk_idx} has insufficient mitigation"

                # Check severity sorting (critical first, then high, then medium, then low)
                severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
                for i in range(len(risks) - 1):
                    current_severity = severity_order[risks[i].severity]
                    next_severity = severity_order[risks[i + 1].severity]
                    assert current_severity <= next_severity, \
                        f"Risks not sorted by severity: {risks[i].severity} before {risks[i+1].severity}"

                results.append({
                    "test_case": idx,
                    "idea": test_case["idea"][:100],
                    "status": "SUCCESS",
                    "swot_items": sum([
                        len(swot.strengths),
                        len(swot.weaknesses),
                        len(swot.opportunities),
                        len(swot.threats)
                    ]),
                    "risk_count": len(risks)
                })

                logger.info(f"✓ [{idx}/20] SUCCESS - SWOT: {results[-1]['swot_items']} items, Risks: {results[-1]['risk_count']}")

            except Exception as e:
                logger.error(f"✗ [{idx}/20] FAILED - {type(e).__name__}: {str(e)}")
                failures.append({
                    "test_case": idx,
                    "idea": test_case["idea"][:100],
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })
                results.append({
                    "test_case": idx,
                    "idea": test_case["idea"][:100],
                    "status": "FAILED",
                    "error": str(e)
                })

        # Calculate metrics
        success_count = len([r for r in results if r["status"] == "SUCCESS"])
        failure_count = len(failures)
        error_rate = (failure_count / len(DIVERSE_PRODUCT_IDEAS)) * 100

        logger.info("\n" + "=" * 80)
        logger.info("SWOT AGENT RELIABILITY TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total runs: {len(DIVERSE_PRODUCT_IDEAS)}")
        logger.info(f"Successful: {success_count} ({100 - error_rate:.1f}%)")
        logger.info(f"Failed: {failure_count} ({error_rate:.1f}%)")
        logger.info(f"Target: <5% error rate (≥19 successful runs)")
        logger.info("=" * 80)

        if failures:
            logger.error("\nFAILURE DETAILS:")
            for failure in failures:
                logger.error(f"\nTest Case {failure['test_case']}: {failure['idea']}")
                logger.error(f"  Error: {failure['error_type']} - {failure['error_message']}")

        # Assert <5% error rate (≥19 successful runs)
        assert success_count >= 19, \
            f"Error rate {error_rate:.1f}% exceeds 5% threshold. Only {success_count}/20 runs succeeded."

        logger.info("\n✓ RELIABILITY TEST PASSED - Error rate within acceptable threshold")

    @pytest.mark.asyncio
    async def test_swot_agent_spanish_input(self):
        """Specific test for Spanish language input (regression test for issue #1990)"""
        adapter = PydanticAgentAdapter()

        spanish_idea = "Plataforma de automatización de clínicas dentales con IA para gestión de citas y comunicación con pacientes"
        strategic_input = "Validación de producto dental automatizado"

        result = await adapter.analyze_swot_risks(spanish_idea, strategic_input)

        # Validate structure (result contains Pydantic objects)
        assert "swot" in result
        assert "risks" in result
        assert len(result["swot"].strengths) >= 3
        assert 4 <= len(result["risks"]) <= 7

        logger.info("✓ Spanish language input test passed")

    @pytest.mark.asyncio
    async def test_swot_agent_vague_input(self):
        """Test with intentionally vague product idea"""
        adapter = PydanticAgentAdapter()

        vague_idea = "An app to help people be more productive"
        strategic_input = "Productivity app validation"

        result = await adapter.analyze_swot_risks(vague_idea, strategic_input)

        # Even with vague input, should produce structured output (Pydantic objects)
        assert "swot" in result
        assert "risks" in result
        assert len(result["swot"].strengths) >= 3
        assert 4 <= len(result["risks"]) <= 7

        logger.info("✓ Vague input test passed")

    @pytest.mark.asyncio
    async def test_swot_agent_highly_technical_input(self):
        """Test with highly technical blockchain product"""
        adapter = PydanticAgentAdapter()

        technical_idea = "Blockchain-based supply chain verification system for pharmaceutical companies using zero-knowledge proofs"
        strategic_input = "Enterprise blockchain validation"

        result = await adapter.analyze_swot_risks(technical_idea, strategic_input)

        # Validate structure (Pydantic objects)
        assert "swot" in result
        assert "risks" in result
        assert len(result["swot"].strengths) >= 3
        assert 4 <= len(result["risks"]) <= 7

        # Should include technical risks
        risk_categories = [r.category for r in result["risks"]]
        assert "technical" in risk_categories or "regulatory" in risk_categories, \
            "Technical product should have technical or regulatory risks"

        logger.info("✓ Highly technical input test passed")

    @pytest.mark.asyncio
    async def test_swot_agent_detailed_specification(self):
        """Test with extremely detailed product specification"""
        adapter = PydanticAgentAdapter()

        detailed_idea = """Real-time collaborative code review platform with AI-powered security vulnerability detection, integrated with GitHub/GitLab/Bitbucket.
        Features: (1) Live code review sessions with video chat, (2) ML models trained on OWASP Top 10 and CWE database detecting vulnerabilities with 92% accuracy,
        (3) Automated fix suggestions using GPT-4-based code generation, (4) Compliance reporting for SOC2/ISO27001/HIPAA."""
        strategic_input = "Developer tools platform validation"

        result = await adapter.analyze_swot_risks(detailed_idea, strategic_input)

        # Validate structure (Pydantic objects)
        assert "swot" in result
        assert "risks" in result
        assert len(result["swot"].strengths) >= 3
        assert 4 <= len(result["risks"]) <= 7

        logger.info("✓ Detailed specification test passed")
