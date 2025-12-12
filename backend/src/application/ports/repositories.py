from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import User, ProductIdea, ResearchResult

class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

class ProductIdeaRepository(ABC):
    @abstractmethod
    async def create(self, idea: ProductIdea) -> ProductIdea:
        pass

    @abstractmethod
    async def get_by_id(self, idea_id: str) -> Optional[ProductIdea]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[ProductIdea]:
        pass

class ResearchResultRepository(ABC):
    @abstractmethod
    async def create(self, result: ResearchResult) -> ResearchResult:
        pass

    @abstractmethod
    async def get_by_idea_id(self, idea_id: str) -> Optional[ResearchResult]:
        pass
