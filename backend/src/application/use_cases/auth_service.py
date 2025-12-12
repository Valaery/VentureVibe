from typing import Optional
from src.domain.entities import User
from src.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from src.application.ports.repositories import UserRepository
from src.infrastructure.web.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(email)
        
        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        return await self.user_repository.create(new_user)

    async def login_user(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
