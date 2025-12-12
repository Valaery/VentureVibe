from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid
from src.domain.value_objects import Email, HashedPassword, Content, FeasibilityScore

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: Email
    hashed_password: HashedPassword
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class ProductIdea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    content: Content
    target_audience: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentThought(BaseModel):
    agent_name: str
    thought: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ResearchResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    idea_id: str
    market_analysis: str
    feasibility_score: FeasibilityScore
    competitors: List[str] = []
    strategic_advice: str
    agent_thoughts: List[AgentThought] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
