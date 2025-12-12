import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from src.main import app
from src.infrastructure.web.dependencies import get_auth_service
from src.domain.entities import User
from src.domain.value_objects import Email, HashedPassword
from src.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException

client = TestClient(app)

@pytest.mark.unit
@pytest.mark.auth
class TestAuthRouter:
    @pytest.fixture
    def mock_auth_service(self):
        return AsyncMock()

    @pytest.fixture
    def override_dependency(self, mock_auth_service):
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        yield
        app.dependency_overrides = {}

    def test_register_success(self, override_dependency, mock_auth_service):
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
        mock_user = User(
            email=Email(root="test@example.com"),
            hashed_password=HashedPassword(root="hashed"),
            full_name="Test User"
        )
        # The router expects the service to return a User object, which is then serialized to UserRead
        mock_auth_service.register_user.return_value = mock_user

        # Act
        response = client.post("/auth/register", json=user_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert "password" not in data
        mock_auth_service.register_user.assert_called_once_with("test@example.com", "password123", "Test User")

    def test_register_duplicate_email(self, override_dependency, mock_auth_service):
        # Arrange
        user_data = {"email": "exists@example.com", "password": "pass"}
        mock_auth_service.register_user.side_effect = UserAlreadyExistsException("exists@example.com")

        # Act
        response = client.post("/auth/register", json=user_data)

        # Assert
        assert response.status_code == 400
        assert "User with email exists@example.com already exists" in response.json()["detail"]

    def test_login_success(self, override_dependency, mock_auth_service):
        # Arrange
        form_data = {
            "username": "test@example.com",
            "password": "password123"
        }
        token_data = {"access_token": "fake_token", "token_type": "bearer"}
        mock_auth_service.login_user.return_value = token_data

        # Act
        response = client.post("/auth/token", data=form_data)

        # Assert
        assert response.status_code == 200
        assert response.json() == token_data
        mock_auth_service.login_user.assert_called_once_with("test@example.com", "password123")

    def test_login_invalid_credentials(self, override_dependency, mock_auth_service):
        # Arrange
        form_data = {"username": "test@example.com", "password": "wrong"}
        mock_auth_service.login_user.side_effect = InvalidCredentialsException()

        # Act
        response = client.post("/auth/token", data=form_data)

        # Assert
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"
