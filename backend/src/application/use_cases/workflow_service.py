import asyncio
import logging
from typing import Optional
from src.domain.entities import ProductIdea, ResearchResult, AgentThought
from src.application.ports.repositories import ProductIdeaRepository, ResearchResultRepository
from src.application.ports.agent_service import AgentService

logger = logging.getLogger(__name__)


class WorkflowService:
    """Orchestrates the 6-agent research pipeline with parallel execution."""

    def __init__(
        self,
        idea_repository: ProductIdeaRepository,
        result_repository: ResearchResultRepository,
        agent_service: AgentService
    ):
        self.idea_repository = idea_repository
        self.result_repository = result_repository
        self.agent_service = agent_service

    async def execute_research(self, user_id: str, content: str, target_audience: str) -> ResearchResult:
        """
        Execute the full 6-agent research pipeline.

        Phase 1 (sequential): Strategist defines direction
        Phase 2 (parallel): 5 specialist agents run concurrently
        """
        # Create and persist the product idea
        idea = ProductIdea(
            user_id=user_id,
            content=content,
            target_audience=target_audience
        )
        await self.idea_repository.create(idea)
        logger.info(f"Created product idea {idea.id} for user {user_id}")

        # Phase 1: Strategic direction (sequential — all other agents need this)
        logger.info("Phase 1: Running Product Strategist...")
        strategy = await self.agent_service.get_strategy(content, target_audience)
        logger.info("Product Strategist completed")

        # Phase 2: Parallel specialist agents (all depend on strategy)
        logger.info("Phase 2: Running 5 specialist agents in parallel...")
        analyst_data, market_sizing, competitive, swot_risk_data, gtm = await asyncio.gather(
            self.agent_service.analyze_market(content, strategy),
            self.agent_service.size_market(content, strategy),
            self.agent_service.analyze_competitors(content, strategy),
            self.agent_service.analyze_swot_risks(content, strategy),
            self.agent_service.develop_gtm(content, strategy),
        )
        logger.info("All 5 specialist agents completed")

        # Construct agent thoughts (simple metadata for now)
        agent_thoughts = [
            AgentThought(
                agent_name="Product Strategist",
                thought="Strategic direction defined with value proposition, customer segments, and success criteria."
            ),
            AgentThought(
                agent_name="Research Analyst",
                thought="Comprehensive market assessment synthesized from all specialist research."
            ),
            AgentThought(
                agent_name="Market Sizing Analyst",
                thought="TAM/SAM/SOM calculated from market research and industry reports."
            ),
            AgentThought(
                agent_name="Competitive Intelligence Analyst",
                thought="Competitor landscape analyzed with positioning and funding data."
            ),
            AgentThought(
                agent_name="SWOT & Risk Analyst",
                thought="SWOT analysis and prioritized risk factors identified."
            ),
            AgentThought(
                agent_name="GTM Strategist",
                thought="Go-to-market strategy developed with ICP, channels, and pricing."
            ),
        ]

        # Construct the research result
        result = ResearchResult(
            idea_id=idea.id,
            executive_summary=analyst_data['executive_summary'],
            market_analysis=analyst_data['market_analysis'],
            strategic_advice=analyst_data['strategic_advice'],
            feasibility_score=analyst_data['feasibility_score'],
            confidence_level=analyst_data['confidence_level'],
            investment_readiness=analyst_data['investment_readiness'],
            key_assumptions=analyst_data['key_assumptions'],
            recommended_next_steps=analyst_data['recommended_next_steps'],
            market_sizing=market_sizing,
            competitive_analysis=competitive,
            swot_analysis=swot_risk_data['swot'],
            risk_factors=swot_risk_data['risks'],
            gtm_strategy=gtm,
            agent_thoughts=agent_thoughts,
        )

        # Persist the research result
        await self.result_repository.create(result)
        logger.info(f"Research result {result.id} saved for idea {idea.id}")

        return result

    async def get_result(self, result_id: str) -> Optional[ResearchResult]:
        """Retrieve a research result by idea ID."""
        return await self.result_repository.get_by_idea_id(result_id)
