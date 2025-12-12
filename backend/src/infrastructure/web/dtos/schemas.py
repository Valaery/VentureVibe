from pydantic import BaseModel, EmailStr
from typing import Optional, List

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

class ResearchResponse(BaseModel):
    id: str
    idea_id: str
    market_analysis: str
    feasibility_score: int
    competitors: List[str]
    strategic_advice: str
