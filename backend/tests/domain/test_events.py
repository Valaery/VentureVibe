import pytest
from datetime import datetime
from src.domain.events import ResearchCompleted, DomainEvent
from src.domain.value_objects import FeasibilityScore

class TestDomainEvents:
    def test_domain_event_base_fields(self):
        event = DomainEvent()
        assert event.event_id is not None
        assert isinstance(event.occurred_at, datetime)

    def test_research_completed_event_creation(self):
        score = FeasibilityScore(root=90)
        event = ResearchCompleted(
            result_id="res_123",
            idea_id="idea_123",
            user_id="user_123",
            feasibility_score=score
        )
        
        assert event.result_id == "res_123"
        assert int(event.feasibility_score) == 90
        assert event.event_id is not None
        assert isinstance(event.occurred_at, datetime)
