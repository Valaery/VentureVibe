from typing import Optional, List
from src.domain.entities import ProductIdea, ResearchResult
from src.application.ports.repositories import ProductIdeaRepository, ResearchResultRepository
from src.infrastructure.database import get_database

class MongoProductIdeaRepository(ProductIdeaRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.product_ideas

    async def create(self, idea: ProductIdea) -> ProductIdea:
        await self.collection.insert_one(idea.model_dump())
        return idea

    async def get_by_id(self, idea_id: str) -> Optional[ProductIdea]:
        doc = await self.collection.find_one({"id": idea_id})
        if doc:
            return ProductIdea(**doc)
        return None

    async def get_by_user_id(self, user_id: str) -> List[ProductIdea]:
        cursor = self.collection.find({"user_id": user_id})
        ideas = []
        async for doc in cursor:
            ideas.append(ProductIdea(**doc))
        return ideas

class MongoResearchResultRepository(ResearchResultRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.research_results

    async def create(self, result: ResearchResult) -> ResearchResult:
        await self.collection.insert_one(result.model_dump())
        return result

    async def get_by_idea_id(self, idea_id: str) -> Optional[ResearchResult]:
        doc = await self.collection.find_one({"idea_id": idea_id})
        if doc:
            return ResearchResult(**doc)
        return None
