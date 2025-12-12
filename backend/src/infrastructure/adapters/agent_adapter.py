from pydantic_ai import Agent
from src.application.ports.agent_service import AgentService
from src.config.settings import settings
import os

# Define response models if needed, or use dicts
from pydantic import BaseModel, Field
from typing import List

class MarketAnalysisResponse(BaseModel):
    market_analysis: str
    feasibility_score: int
    competitors: List[str]
    strategic_advice: str

class PydanticAgentAdapter(AgentService):
    def __init__(self):
        # Initialize agents with OpenRouter model
        # Pydantic AI uses the 'openai:' prefix for OpenAI-compatible endpoints
        # We need to ensure the environment variables for OPENAI_API_KEY and OPENAI_BASE_URL are set
        # or pass them explicitly if Pydantic AI supports it directly in the model string or config.
        # Assuming standard env vars or OpenAIModel config.
        
        # Using the requested model
        model_name = 'openai:google/gemini-2.5-flash-lite'
        
        self.strategist_agent = Agent(
            model_name,
            system_prompt="You are an expert Product Strategist. Your goal is to refine product ideas and define a high-level strategy.",
            result_type=str
        )
        
        self.analyst_agent = Agent(
            model_name,
            system_prompt="You are a senior Research Analyst. Analyze the market, competitors, and feasibility based on the idea and strategy.",
            result_type=MarketAnalysisResponse
        )

        # Explicitly set the base URL if needed for the underlying client, 
        # though Pydantic AI usually picks up OPENAI_BASE_URL env var.
        # For safety, we can set it in os.environ if not already there, 
        # but settings.py loads from .env, so we trust environment setup or settings usage.
        if settings.OPENAI_BASE_URL and settings.OPENAI_API_KEY:
            os.environ["OPENAI_BASE_URL"] = settings.OPENAI_BASE_URL
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

    async def _run_with_retry(self, agent: Agent, prompt: str, retries: int = 3):
        headers = {} # Fix: Unexpected keyword argument 'headers' for Agent.run? PydanticAI Agent.run takes deps not headers usually. 
        # Actually PydanticAI v0.0.x might differ. Let's assume standard run.
        # But we need to handle exceptions.
        last_exception = None
        for attempt in range(retries):
            try:
                return await agent.run(prompt)
            except Exception as e:
                last_exception = e
                # Simple exponential backoff or constant
                import asyncio
                await asyncio.sleep(1 * (attempt + 1))
        raise last_exception

    async def get_strategy(self, idea_content: str, audience: str) -> str:
        prompt = f"Idea: {idea_content}\nTarget Audience: {audience}\n\nRefine this idea and provide a strategic direction."
        result = await self._run_with_retry(self.strategist_agent, prompt)
        return result.data

    async def analyze_market(self, idea_content: str, strategy: str) -> dict:
        prompt = f"Idea: {idea_content}\nStrategy: {strategy}\n\nProvide market analysis, feasibility score (0-100), competitors, and advice."
        result = await self._run_with_retry(self.analyst_agent, prompt)
        return result.data.model_dump()
