from abc import ABC, abstractmethod
from typing import Dict, Any
from src.domain.entities import MarketSizing, CompetitiveAnalysis, GTMStrategy


class AgentService(ABC):

    @abstractmethod
    async def get_strategy(self, idea_content: str, audience: str) -> str:
        """Get strategic direction from the Product Strategist agent."""
        pass

    @abstractmethod
    async def analyze_market(self, idea_content: str, strategy: str) -> Dict[str, Any]:
        """Synthesize comprehensive market assessment. Returns AnalystOutput fields as dict."""
        pass

    @abstractmethod
    async def size_market(self, idea_content: str, strategy: str) -> MarketSizing:
        """Research and calculate TAM/SAM/SOM using web search tools."""
        pass

    @abstractmethod
    async def analyze_competitors(self, idea_content: str, strategy: str) -> CompetitiveAnalysis:
        """Identify and analyze competitors using web search tools."""
        pass

    @abstractmethod
    async def analyze_swot_risks(self, idea_content: str, strategy: str) -> Dict[str, Any]:
        """Conduct SWOT analysis and identify risk factors. Returns {swot, risks} dict."""
        pass

    @abstractmethod
    async def develop_gtm(self, idea_content: str, strategy: str) -> GTMStrategy:
        """Design a go-to-market strategy."""
        pass
