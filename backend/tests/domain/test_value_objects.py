import pytest
from pydantic import ValidationError
from src.domain.value_objects import Email, FeasibilityScore, Password, HashedPassword, Content

class TestEmailValueObject:
    def test_valid_email(self):
        email = Email(root="test@example.com")
        assert str(email) == "test@example.com"
        assert email.root == "test@example.com"

    def test_invalid_email_format(self):
        with pytest.raises(ValidationError):
            Email(root="invalid-email")

    def test_email_equality(self):
        email1 = Email(root="test@example.com")
        email2 = Email(root="test@example.com")
        assert email1 == email2

class TestFeasibilityScoreValueObject:
    def test_valid_score(self):
        score = FeasibilityScore(root=85)
        assert int(score) == 85

    def test_score_lower_bound(self):
        score = FeasibilityScore(root=0)
        assert int(score) == 0

    def test_score_upper_bound(self):
        score = FeasibilityScore(root=100)
        assert int(score) == 100

    def test_score_below_zero_raises_error(self):
        with pytest.raises(ValidationError):
            FeasibilityScore(root=-1)

    def test_score_above_hundred_raises_error(self):
        with pytest.raises(ValidationError):
            FeasibilityScore(root=101)

class TestPasswordValueObject:
    def test_valid_password(self):
        pw = Password(root="securepassword")
        assert pw.root == "securepassword"

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            Password(root="short")

    def test_str_representation_is_masked(self):
        pw = Password(root="securepassword")
        assert str(pw) == "***"

class TestHashedPasswordValueObject:
    def test_hashed_password_creation(self):
        hashed = HashedPassword(root="hashed_value")
        assert hashed.root == "hashed_value"
        assert str(hashed) == "hashed_value"

class TestContentValueObject:
    def test_valid_content(self):
        content = Content(root="This is a valid product idea content.")
        assert content.root == "This is a valid product idea content."
        assert str(content) == "This is a valid product idea content."

    def test_content_too_short(self):
        with pytest.raises(ValidationError) as exc:
            Content(root="Short")
        assert "Product idea must be at least 10 characters long" in str(exc.value)

    def test_content_strips_whitespace_for_validation(self):
        with pytest.raises(ValidationError):
            Content(root="   Short   ")
