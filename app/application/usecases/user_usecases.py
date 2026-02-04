"""User CRUD use cases module."""

from datetime import datetime
from typing import List, Optional

from app.domain.entities.user import User, UserRole, ForceAlignment
from app.domain.errors import NotFoundError, DuplicateError
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.service.auth_service import AuthService, get_auth_service


class CreateUserUseCase:
    """Use case for creating a new common user."""

    def __init__(
        self,
        repository: UserRepository,
        auth_service: Optional[AuthService] = None,
    ):
        """Initialize with dependencies."""
        self.repository = repository
        self.auth_service = auth_service or get_auth_service()

    async def execute(
        self,
        username: str,
        email: str,
        password: str,
        alignment: ForceAlignment,
        full_name: Optional[str] = None,
    ) -> User:
        """Create a new common user."""
        # Check for existing username
        existing = await self.repository.get_by_username(username)
        if existing:
            raise DuplicateError("User", "username", username)

        # Check for existing email
        existing = await self.repository.get_by_email(email)
        if existing:
            raise DuplicateError("User", "email", email)

        # Create user with hashed password
        user = User(
            username=username,
            email=email,
            hashed_password=self.auth_service.hash_password(password),
            full_name=full_name,
            is_active=True,
            is_superuser=False,
            role=UserRole.USER,
            alignment=alignment,
            created_at=datetime.utcnow(),
        )

        return await self.repository.create(user)


class CreateAdminUserUseCase:
    """Use case for creating an admin user (only callable by admins)."""

    def __init__(
        self,
        repository: UserRepository,
        auth_service: Optional[AuthService] = None,
    ):
        """Initialize with dependencies."""
        self.repository = repository
        self.auth_service = auth_service or get_auth_service()

    async def execute(
        self,
        username: str,
        email: str,
        password: str,
        alignment: ForceAlignment,
        full_name: Optional[str] = None,
    ) -> User:
        """Create a new admin user."""
        # Check for existing username
        existing = await self.repository.get_by_username(username)
        if existing:
            raise DuplicateError("User", "username", username)

        # Check for existing email
        existing = await self.repository.get_by_email(email)
        if existing:
            raise DuplicateError("User", "email", email)

        # Create admin user with hashed password
        user = User(
            username=username,
            email=email,
            hashed_password=self.auth_service.hash_password(password),
            full_name=full_name,
            is_active=True,
            is_superuser=True,
            role=UserRole.ADMIN,
            alignment=alignment,
            created_at=datetime.utcnow(),
        )

        return await self.repository.create(user)


class GetUserByIdUseCase:
    """Use case for getting a user by ID."""

    def __init__(self, repository: UserRepository):
        """Initialize with repository."""
        self.repository = repository

    async def execute(self, user_id: str) -> User:
        """Get a user by ID."""
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user


class GetAllUsersUseCase:
    """Use case for getting all users."""

    def __init__(self, repository: UserRepository):
        """Initialize with repository."""
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 100) -> tuple[List[User], int]:
        """Get all users with pagination."""
        users = await self.repository.get_all(skip=skip, limit=limit)
        count = await self.repository.count()
        return users, count


class UpdateUserUseCase:
    """Use case for updating a user."""

    def __init__(
        self,
        repository: UserRepository,
        auth_service: Optional[AuthService] = None,
    ):
        """Initialize with dependencies."""
        self.repository = repository
        self.auth_service = auth_service or get_auth_service()

    async def execute(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        full_name: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> User:
        """Update a user."""
        # Check user exists
        existing = await self.repository.get_by_id(user_id)
        if existing is None:
            raise NotFoundError("User", user_id)

        # Build update data
        update_data = {}
        
        if username is not None and username != existing.username:
            # Check username not taken
            conflict = await self.repository.get_by_username(username)
            if conflict:
                raise DuplicateError("User", "username", username)
            update_data["username"] = username

        if email is not None and email != existing.email:
            # Check email not taken
            conflict = await self.repository.get_by_email(email)
            if conflict:
                raise DuplicateError("User", "email", email)
            update_data["email"] = email

        if password is not None:
            update_data["hashed_password"] = self.auth_service.hash_password(password)

        if full_name is not None:
            update_data["full_name"] = full_name

        if is_active is not None:
            update_data["is_active"] = is_active

        if not update_data:
            return existing

        user = await self.repository.update(user_id, update_data)
        if user is None:
            raise NotFoundError("User", user_id)
        return user


class DeleteUserUseCase:
    """Use case for deleting a user."""

    def __init__(self, repository: UserRepository):
        """Initialize with repository."""
        self.repository = repository

    async def execute(self, user_id: str) -> bool:
        """Delete a user."""
        existing = await self.repository.get_by_id(user_id)
        if existing is None:
            raise NotFoundError("User", user_id)
        
        return await self.repository.delete(user_id)
