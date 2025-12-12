from abc import ABC, abstractmethod
from src.domain.entities import ProductIdea, ResearchResult

class AgentService(ABC):
    @abstractmethod
    async def get_strategy(self, idea_content: str, audience: str) -> str:
        """Get feedback/strategy from the Product Strategist agent."""
        pass
    
    @abstractmethod
    async def analyze_market(self, idea_content: str, strategy: str) -> dict:
        """Get market analysis from the Research Analyst agent."""
        pass
