"""Auth router module."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token, RefreshTokenRequest
from app.domain.errors import AuthenticationError
from app.infrastructure.db.database import get_database
from app.infrastructure.repositories.user_repository import (
    UserRepository,
    RefreshTokenRepository,
)
from app.application.usecases.auth_usecases import LoginUseCase, RefreshTokenUseCase


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=Token,
    summary="Login",
    description="Authenticate user and get access and refresh tokens.",
)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate user and return tokens."""
    db = get_database()
    user_repository = UserRepository(db)
    token_repository = RefreshTokenRepository(db)

    use_case = LoginUseCase(
        user_repository=user_repository,
        token_repository=token_repository,
    )

    try:
        result = await use_case.execute(
            username=form_data.username,
            password=form_data.password,
        )
        return result
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh token",
    description="Refresh access token using a valid refresh token.",
)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token."""
    db = get_database()
    user_repository = UserRepository(db)
    token_repository = RefreshTokenRepository(db)

    use_case = RefreshTokenUseCase(
        user_repository=user_repository,
        token_repository=token_repository,
    )

    try:
        result = await use_case.execute(refresh_token_value=request.refresh_token)
        return result
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
