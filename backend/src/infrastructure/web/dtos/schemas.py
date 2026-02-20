from pydantic import BaseModel, EmailStr
from typing import Optional, List, Literal
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class ResearchRequest(BaseModel):
    content: str
    target_audience: Optional[str] = "General Public"


# New domain-aligned schemas for rich research results
class MarketSizingSchema(BaseModel):
    tam_usd_billion: float
    sam_usd_billion: float
    som_usd_million: float
    sizing_methodology: Literal["top_down", "bottom_up", "hybrid"]
    tam_source_basis: str
    growth_rate_pct: Optional[float] = None


class CompetitorSchema(BaseModel):
    name: str
    positioning: str
    primary_weakness: str
    estimated_funding_usd_million: Optional[float] = None
    business_model: str


class CompetitiveAnalysisSchema(BaseModel):
    direct_competitors: List[CompetitorSchema]
    indirect_competitors: List[CompetitorSchema]
    competitive_moat: str
    differentiation_score: int


class SWOTAnalysisSchema(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class RiskFactorSchema(BaseModel):
    category: Literal["market", "technical", "regulatory", "competitive", "financial", "execution"]
    description: str
    severity: Literal["low", "medium", "high", "critical"]
    mitigation: str


class GTMStrategySchema(BaseModel):
    primary_channel: str
    secondary_channels: List[str]
    pricing_model: str
    estimated_cac_usd: Optional[float] = None
    target_icp: str
    time_to_first_revenue_months: int


class AgentThoughtSchema(BaseModel):
    agent_name: str
    thought: str
    timestamp: datetime


class ResearchResponse(BaseModel):
    id: str
    idea_id: str
    executive_summary: str
    market_analysis: str
    strategic_advice: str
    key_assumptions: List[str]
    recommended_next_steps: List[str]
    feasibility_score: int
    confidence_level: Literal["low", "medium", "high"]
    investment_readiness: Literal["pre_idea", "idea_stage", "mvp_ready", "seed_ready", "series_a_ready"]
    market_sizing: MarketSizingSchema
    competitive_analysis: CompetitiveAnalysisSchema
    swot_analysis: SWOTAnalysisSchema
    risk_factors: List[RiskFactorSchema]
    gtm_strategy: GTMStrategySchema
    agent_thoughts: List[AgentThoughtSchema] = []
