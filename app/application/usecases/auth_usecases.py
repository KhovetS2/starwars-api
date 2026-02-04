"""Auth use cases module."""

from typing import Optional

from app.domain.entities.user import User, RefreshToken
from app.domain.errors import AuthenticationError
from app.infrastructure.repositories.user_repository import (
    UserRepository,
    RefreshTokenRepository,
)
from app.application.service.auth_service import AuthService, get_auth_service, get_user_scopes
from app.schemas.auth import Token


class LoginUseCase:
    """Use case for user login."""

    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: RefreshTokenRepository,
        auth_service: Optional[AuthService] = None,
    ):
        """Initialize with dependencies."""
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.auth_service = auth_service or get_auth_service()

    async def execute(self, username: str, password: str) -> Token:
        """Authenticate user and return tokens."""
        # Find user by username
        user = await self.user_repository.get_by_username(username)
        
        if user is None:
            raise AuthenticationError("Invalid username or password")

        # Verify password
        if not self.auth_service.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid username or password")

        # Check if user is active
        if not user.is_active:
            raise AuthenticationError("User account is disabled")

        # Get user scopes based on role
        scopes = get_user_scopes(user)

        # Create access token with scopes
        access_token = self.auth_service.create_access_token(
            user_id=user.id,
            username=user.username,
            scopes=scopes,
        )

        # Create refresh token
        refresh_token = self.auth_service.create_refresh_token(user_id=user.id)
        await self.token_repository.create(refresh_token)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token.token,
            token_type="bearer",
        )


class RefreshTokenUseCase:
    """Use case for refreshing access token."""

    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: RefreshTokenRepository,
        auth_service: Optional[AuthService] = None,
    ):
        """Initialize with dependencies."""
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.auth_service = auth_service or get_auth_service()

    async def execute(self, refresh_token_value: str) -> Token:
        """Refresh access token using refresh token."""
        # Get refresh token
        refresh_token = await self.token_repository.get_by_token(refresh_token_value)
        
        if refresh_token is None:
            raise AuthenticationError("Invalid refresh token")

        # Validate refresh token
        if not self.auth_service.is_refresh_token_valid(refresh_token):
            raise AuthenticationError("Refresh token is expired or revoked")

        # Get user
        user = await self.user_repository.get_by_id(refresh_token.user_id)
        
        if user is None:
            raise AuthenticationError("User not found")

        if not user.is_active:
            raise AuthenticationError("User account is disabled")

        # Revoke old refresh token
        await self.token_repository.revoke(refresh_token_value)

        # Get user scopes based on role
        scopes = get_user_scopes(user)

        # Create new access token with scopes
        access_token = self.auth_service.create_access_token(
            user_id=user.id,
            username=user.username,
            scopes=scopes,
        )

        # Create new refresh token
        new_refresh_token = self.auth_service.create_refresh_token(user_id=user.id)
        await self.token_repository.create(new_refresh_token)

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token.token,
            token_type="bearer",
        )


class LogoutUseCase:
    """Use case for user logout (revoke tokens)."""

    def __init__(self, token_repository: RefreshTokenRepository):
        """Initialize with dependencies."""
        self.token_repository = token_repository

    async def execute(self, user_id: str) -> int:
        """Revoke all refresh tokens for user."""
        return await self.token_repository.revoke_all_for_user(user_id)
