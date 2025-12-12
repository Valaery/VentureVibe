import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.application.use_cases.auth_service import AuthService
from src.domain.entities import User
from src.domain.value_objects import Email, HashedPassword
from src.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException

class TestAuthService:
    @pytest.fixture
    def mock_user_repo(self):
        return AsyncMock()

    @pytest.fixture
    def auth_service(self, mock_user_repo):
        return AuthService(mock_user_repo)

    @patch('src.application.use_cases.auth_service.get_password_hash')
    async def test_register_user_success(self, mock_hash, auth_service, mock_user_repo):
        # Arrange
        email = "test@example.com"
        password = "password123"
        mock_user_repo.get_by_email.return_value = None
        mock_hash.return_value = HashedPassword(root="hashed_secret")
        # Ensure create returns the user passed to it (simulate repo behavior)
        mock_user_repo.create.side_effect = lambda u: u

        # Act
        user = await auth_service.register_user(email, password, full_name="Test User")

        # Assert
        assert user.email.root == email
        assert user.full_name == "Test User"
        assert user.hashed_password.root == "hashed_secret"
        mock_user_repo.get_by_email.assert_called_once_with(email)
        mock_user_repo.create.assert_called_once()

    @patch('src.application.use_cases.auth_service.get_password_hash')
    async def test_register_user_already_exists(self, mock_hash, auth_service, mock_user_repo):
        # Arrange
        email = "exist@example.com"
        existing_user = User(
            email=Email(root=email),
            hashed_password=HashedPassword(root="hashed")
        )
        mock_user_repo.get_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException):
            await auth_service.register_user(email, "password")
        
        mock_user_repo.create.assert_not_called()

    @patch('src.application.use_cases.auth_service.create_access_token')
    @patch('src.application.use_cases.auth_service.verify_password')
    async def test_login_user_success(self, mock_verify, mock_token, auth_service, mock_user_repo):
        # Arrange
        email = "test@example.com"
        password = "password123"
        user = User(
            email=Email(root=email),
            hashed_password=HashedPassword(root="hashed_secret")
        )
        mock_user_repo.get_by_email.return_value = user
        mock_verify.return_value = True
        mock_token.return_value = "fake_jwt_token"

        # Act
        result = await auth_service.login_user(email, password)

        # Assert
        assert result["access_token"] == "fake_jwt_token"
        assert result["token_type"] == "bearer"
        mock_verify.assert_called_once()

    @patch('src.application.use_cases.auth_service.verify_password')
    async def test_login_user_invalid_credentials_password(self, mock_verify, auth_service, mock_user_repo):
        # Arrange
        email = "test@example.com"
        user = User(
            email=Email(root=email),
            hashed_password=HashedPassword(root="hashed_secret")
        )
        mock_user_repo.get_by_email.return_value = user
        mock_verify.return_value = False

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.login_user(email, "wrong_password")

    async def test_login_user_not_found(self, auth_service, mock_user_repo):
        # Arrange
        mock_user_repo.get_by_email.return_value = None

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.login_user("unknown@example.com", "password")
