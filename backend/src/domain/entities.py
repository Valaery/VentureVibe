from datetime import datetime
from typing import Optional, List
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

class ResearchResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    idea_id: str
    market_analysis: str
    feasibility_score: int = Field(ge=0, le=100)
    competitors: List[str] = []
    strategic_advice: str
    agent_thoughts: List[AgentThought] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
