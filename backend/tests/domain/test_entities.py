import pytest
from datetime import datetime
from src.domain.entities import User, ProductIdea, ResearchResult, AgentThought
from src.domain.value_objects import Email, HashedPassword, Content, FeasibilityScore

class TestUserEntity:
    def test_create_user_success(self):
        email = Email(root="user@example.com")
        password = HashedPassword(root="hashed_secret")
        user = User(email=email, hashed_password=password, full_name="John Doe")
        
        assert user.id is not None
        assert user.email == email
        assert user.hashed_password == password
        assert user.full_name == "John Doe"
        assert user.created_at is not None
        assert user.is_active is True

    def test_create_user_defaults(self):
        email = Email(root="user@example.com")
        password = HashedPassword(root="hashed_secret")
        user = User(email=email, hashed_password=password)
        
        assert user.full_name is None
        assert user.is_active is True

class TestProductIdeaEntity:
    def test_create_product_idea_success(self):
        content = Content(root="A revolutionary new toaster")
        idea = ProductIdea(user_id="user_123", content=content, target_audience="Home clicks")
        
        assert idea.id is not None
        assert idea.user_id == "user_123"
        assert idea.content == content
        assert idea.target_audience == "Home clicks"
        assert idea.created_at is not None

class TestResearchResultEntity:
    def test_create_research_result_success(self):
        score = FeasibilityScore(root=85)
        thought = AgentThought(agent_name="MarketAgent", thought="Looks good")
        
        result = ResearchResult(
            idea_id="idea_123",
            market_analysis="Detailed analysis...",
            feasibility_score=score,
            competitors=["Comp A", "Comp B"],
            strategic_advice="Go for it",
            agent_thoughts=[thought]
        )
        
        assert result.id is not None
        assert result.idea_id == "idea_123"
        assert int(result.feasibility_score) == 85
        assert len(result.competitors) == 2
        assert len(result.agent_thoughts) == 1
        assert result.agent_thoughts[0].agent_name == "MarketAgent"
