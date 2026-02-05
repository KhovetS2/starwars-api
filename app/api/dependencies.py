"""API dependencies module."""

from typing import Annotated, List

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.domain.entities.user import User
from app.application.service.auth_service import get_auth_service, AuthService, SCOPES
from app.infrastructure.db.database import get_database
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.message_repository import MessageRepository


# OAuth2 scheme with scopes
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scopes=SCOPES,
)


async def get_user_repository() -> UserRepository:
    """Get user repository dependency."""
    db = get_database()
    return UserRepository(db)


async def get_message_repository() -> MessageRepository:
    """Get message repository dependency."""
    db = get_database()
    return MessageRepository(db)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """Dependency to get the current authenticated user with scope validation."""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    token_data = auth_service.decode_access_token(token)
    if token_data is None:
        raise credentials_exception

    user = await user_repository.get_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception

    # Validate scopes
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


async def get_current_active_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """Dependency to get the current active user with scope validation."""
    current_user = await get_current_user(
        security_scopes=security_scopes,
        token=token,
        auth_service=auth_service,
        user_repository=user_repository,
    )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:admin"])],
) -> User:
    """Dependency to get the current superuser (with admin scope)."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
