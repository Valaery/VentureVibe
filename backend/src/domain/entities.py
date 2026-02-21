from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
import uuid


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class ProductIdea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    content: str
    target_audience: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode='after')
    def validate_content(self):
        if len(self.content.strip()) < 10:
            raise ValueError("Product idea must be at least 10 characters long")
        return self


class AgentThought(BaseModel):
    agent_name: str
    thought: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MarketSizing(BaseModel):
    tam_usd_billion: float = Field(description="Total Addressable Market in USD Billions")
    sam_usd_billion: float = Field(description="Serviceable Addressable Market in USD Billions")
    som_usd_million: float = Field(description="Serviceable Obtainable Market (3-year estimate) in USD Millions")
    sizing_methodology: Literal["top_down", "bottom_up", "hybrid"] = Field(description="The approach used to calculate numbers")
    tam_source_basis: str = Field(description="The source or rationale for the TAM figure")
    growth_rate_pct: Optional[float] = Field(default=None, description="Projected annual market growth rate percentage")


class Competitor(BaseModel):
    name: str = Field(description="Real company name")
    positioning: str = Field(description="One-sentence value proposition")
    primary_weakness: str = Field(description="Specific exploitabe gap or customer pain point they ignore")
    estimated_funding_usd_million: Optional[float] = Field(default=0.0, description="Total funding raised in USD Millions. Use 0.0 if unknown.")
    business_model: str = Field(description="The revenue model (e.g. B2B SaaS, Marketplace)")


class CompetitiveAnalysis(BaseModel):
    direct_competitors: List[Competitor]
    indirect_competitors: List[Competitor]
    competitive_moat: str
    differentiation_score: int  # 1-10


class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class RiskFactor(BaseModel):
    category: Literal["market", "technical", "regulatory", "competitive", "financial", "execution"] = Field(description="The source area of the risk")
    description: str = Field(description="Detailed explanation of the risk event and impact")
    severity: Literal["low", "medium", "high", "critical"] = Field(description="Impact level of the risk")
    mitigation: str = Field(description="Proposed strategy to manage or avoid the risk")


class GTMStrategy(BaseModel):
    primary_channel: str
    secondary_channels: List[str]
    pricing_model: str
    estimated_cac_usd: Optional[float] = None
    target_icp: str
    time_to_first_revenue_months: int


class ResearchResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    idea_id: str
    # Narrative
    executive_summary: str
    market_analysis: str
    strategic_advice: str
    key_assumptions: List[str]
    recommended_next_steps: List[str]
    # Scores
    feasibility_score: int = Field(ge=0, le=100)
    confidence_level: Literal["low", "medium", "high"]
    investment_readiness: Literal["pre_idea", "idea_stage", "mvp_ready", "seed_ready", "series_a_ready"]
    # Rich sections
    market_sizing: MarketSizing
    competitive_analysis: CompetitiveAnalysis
    swot_analysis: SWOTAnalysis
    risk_factors: List[RiskFactor]
    gtm_strategy: GTMStrategy
    # Meta
    agent_thoughts: List[AgentThought] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
