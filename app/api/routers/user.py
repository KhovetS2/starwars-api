"""Users router module."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query, Security

from app.schemas.user import UserCreate, UserCreateAdmin, UserUpdate, UserResponse, UserListResponse
from app.domain.entities.user import User, UserRole
from app.domain.errors import NotFoundError, DuplicateError
from app.api.dependencies import get_current_active_user, get_user_repository
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.usecases.user_usecases import (
    CreateUserUseCase,
    CreateAdminUserUseCase,
    GetUserByIdUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)


router = APIRouter(prefix="/users", tags=["Users"])


def user_to_response(user: User) -> UserResponse:
    """Convert User entity to UserResponse schema."""
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        role=user.role,
        alignment=user.alignment,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description="Create a new common user account. Requires alignment (light/dark).",
)
async def create_user(
    user_data: UserCreate,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Create a new common user."""
    use_case = CreateUserUseCase(repository=user_repository)
    
    try:
        user = await use_case.execute(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            alignment=user_data.alignment,
            full_name=user_data.full_name,
        )
        return user_to_response(user)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.post(
    "/admin",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create admin user",
    description="Create a new administrator user. Only accessible by existing admins (requires 'users:admin' scope).",
)
async def create_admin_user(
    user_data: UserCreateAdmin,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:admin"])],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Create a new admin user. Only admins can create other admins."""
    use_case = CreateAdminUserUseCase(repository=user_repository)
    
    try:
        user = await use_case.execute(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            alignment=user_data.alignment,
            full_name=user_data.full_name,
        )
        return user_to_response(user)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get all users",
    description="Retrieve a list of all users (requires 'users:read' scope).",
)
async def get_all_users(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    sort_by: Literal["username", "email", "created_at"] = Query("created_at", description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query("desc", description="Sort order: 'asc' or 'desc'"),
):
    """Get all users with pagination and sorting."""
    use_case = GetAllUsersUseCase(repository=user_repository)
    users, count = await use_case.execute(
        skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order
    )
    
    return UserListResponse(
        count=count,
        results=[user_to_response(u) for u in users],
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Retrieve the current authenticated user's information (requires 'users:read' scope).",
)
async def get_current_user_info(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
):
    """Get current user information."""
    return user_to_response(current_user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID (requires 'users:read' scope).",
)
async def get_user_by_id(
    user_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Get a specific user by ID."""
    use_case = GetUserByIdUseCase(repository=user_repository)
    
    try:
        user = await use_case.execute(user_id)
        return user_to_response(user)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update a user's information (requires 'users:write' scope).",
)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:write"])],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Update a user."""
    # Only allow users to update themselves or superusers to update anyone
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update other users",
        )

    use_case = UpdateUserUseCase(repository=user_repository)
    
    try:
        user = await use_case.execute(
            user_id=user_id,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
        )
        return user_to_response(user)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user account (requires 'users:delete' scope).",
)
async def delete_user(
    user_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:delete"])],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Delete a user."""
    # Only allow users to delete themselves or superusers to delete anyone
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete other users",
        )

    use_case = DeleteUserUseCase(repository=user_repository)
    
    try:
        await use_case.execute(user_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
