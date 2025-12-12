from pydantic import BaseModel
from typing import Optional, List
from src.domain.value_objects import Email, FeasibilityScore

class UserCreate(BaseModel):
    email: Email
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: str
    email: Email
    full_name: Optional[str] = None
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class ResearchRequest(BaseModel):
    content: str
    target_audience: Optional[str] = "General Public"

class ResearchResponse(BaseModel):
    id: str
    idea_id: str
    market_analysis: str
    feasibility_score: FeasibilityScore
    competitors: List[str]
    strategic_advice: str
