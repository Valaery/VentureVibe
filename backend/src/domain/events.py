from datetime import datetime
from pydantic import BaseModel, Field
import uuid
from src.domain.value_objects import FeasibilityScore

class DomainEvent(BaseModel):
    """Base class for all domain events."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

class ResearchCompleted(DomainEvent):
    """Event triggered when a product research is completed."""
    result_id: str
    idea_id: str
    user_id: str
    feasibility_score: FeasibilityScore
