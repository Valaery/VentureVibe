from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional

from src.config.settings import settings
from src.application.ports.repositories import UserRepository
from src.infrastructure.adapters.repositories.mongo_user_repository import MongoUserRepository
from src.domain.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_user_repository() -> UserRepository:
    return MongoUserRepository()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_repository.get_by_email(email)
    if user is None:
        raise credentials_exception
    
    return user

from src.application.use_cases.auth_service import AuthService
from src.application.use_cases.workflow_service import WorkflowService
from src.infrastructure.adapters.repositories.mongo_repositories import MongoProductIdeaRepository, MongoResearchResultRepository
from src.infrastructure.adapters.agent_adapter import PydanticAgentAdapter

async def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)

async def get_workflow_service() -> WorkflowService:
    return WorkflowService(
        idea_repository=MongoProductIdeaRepository(),
        result_repository=MongoResearchResultRepository(),
        agent_service=PydanticAgentAdapter()
    )

