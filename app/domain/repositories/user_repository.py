"""User repository interface module."""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User, RefreshToken


class UserRepositoryInterface(ABC):
    """Abstract interface for user repository."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        pass

    @abstractmethod
    async def update(self, user_id: str, user_data: dict) -> Optional[User]:
        """Update a user."""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete a user."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count total users."""
        pass


class RefreshTokenRepositoryInterface(ABC):
    """Abstract interface for refresh token repository."""

    @abstractmethod
    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create a new refresh token."""
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get a refresh token by its value."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[RefreshToken]:
        """Get all refresh tokens for a user."""
        pass

    @abstractmethod
    async def revoke(self, token: str) -> bool:
        """Revoke a refresh token."""
        pass

    @abstractmethod
    async def revoke_all_for_user(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user."""
        pass

    @abstractmethod
    async def delete_expired(self) -> int:
        """Delete all expired tokens."""
        pass
