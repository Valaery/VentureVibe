from pydantic_ai import Agent
from src.application.ports.agent_service import AgentService
from src.config.settings import settings
import os
from pydantic import BaseModel, Field
from typing import List

class MarketAnalysisResponse(BaseModel):
    market_analysis: str
    feasibility_score: int
    competitors: List[str]
    strategic_advice: str

class PydanticAgentAdapter(AgentService):
    def __init__(self):
        # Set environment variables BEFORE initializing agents
        # Pydantic AI agents need these env vars during construction
        if settings.OPENAI_BASE_URL and settings.OPENAI_API_KEY:
            os.environ["OPENAI_BASE_URL"] = settings.OPENAI_BASE_URL
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        

        model_name = settings.LLM_MODEL
        
        self.strategist_agent = Agent[str](
            model_name,
            system_prompt="You are an expert Product Strategist. Your goal is to refine product ideas and define a high-level strategy."
        )
        
        self.analyst_agent = Agent(
            model_name,
            output_type=MarketAnalysisResponse,
            system_prompt="You are a senior Research Analyst. Analyze the market, competitors, and feasibility based on the idea and strategy."
        )

    async def get_strategy(self, idea_content: str, audience: str) -> str:
        prompt = f"Idea: {idea_content}\nTarget Audience: {audience}\n\nRefine this idea and provide a strategic direction."
        result = await self.strategist_agent.run(prompt)
        return result.output

    async def analyze_market(self, idea_content: str, strategy: str) -> dict:
        prompt = f"Idea: {idea_content}\nStrategy: {strategy}\n\nProvide market analysis, feasibility score (0-100), competitors, and advice."
        result = await self.analyst_agent.run(prompt)

        return result.output.model_dump()
