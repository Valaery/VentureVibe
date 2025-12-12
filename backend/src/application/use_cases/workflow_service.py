from typing import Optional
from src.domain.entities import ProductIdea, ResearchResult
from src.application.ports.repositories import ProductIdeaRepository, ResearchResultRepository
from src.application.ports.agent_service import AgentService
import logging

logger = logging.getLogger(__name__)

class WorkflowService:
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

        idea = ProductIdea(
            user_id=user_id,
            content=content,
            target_audience=target_audience
        )
        await self.idea_repository.create(idea)
        logger.info(f"Created idea {idea.id}")


        strategy = await self.agent_service.get_strategy(content, target_audience)
        logger.info("Strategist completed")


        market_data = await self.agent_service.analyze_market(content, strategy)
        logger.info("Analyst completed")


        result = ResearchResult(
            idea_id=idea.id,
            market_analysis=market_data['market_analysis'],
            feasibility_score=market_data['feasibility_score'],
            competitors=market_data['competitors'],
            strategic_advice=market_data['strategic_advice'] + f"\n\nStrategy: {strategy}"
        )


        await self.result_repository.create(result)
        
        return result

    async def get_result(self, result_id: str) -> Optional[ResearchResult]:
        return await self.result_repository.get_by_idea_id(result_id)
