import pytest
from src.domain.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    ProductIdeaNotFoundException,
    ResearchResultNotFoundException
)

class TestDomainExceptions:
    def test_user_already_exists_message(self):
        exc = UserAlreadyExistsException("test@example.com")
        assert str(exc) == "User with email test@example.com already exists"

    def test_invalid_credentials_message(self):
        exc = InvalidCredentialsException()
        assert str(exc) == "Invalid email or password"

    def test_product_idea_not_found_message(self):
        exc = ProductIdeaNotFoundException("idea_123")
        assert str(exc) == "Product idea idea_123 not found"

    def test_research_result_not_found_message(self):
        exc = ResearchResultNotFoundException("res_123")
        assert str(exc) == "Research result res_123 not found"
