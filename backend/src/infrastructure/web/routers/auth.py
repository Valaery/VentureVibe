from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.infrastructure.web.dtos.schemas import UserCreate, UserRead, Token
from src.application.use_cases.auth_service import AuthService
from src.infrastructure.web.dependencies import get_auth_service
from src.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    try:
        user = await auth_service.register_user(user_in.email, user_in.password, user_in.full_name)
        return user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.login_user(form_data.username, form_data.password)
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
