"""User entity module."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User entity for authentication."""

    id: Optional[str] = None
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


@dataclass
class RefreshToken:
    """Refresh token entity for token management."""

    id: Optional[str] = None
    user_id: str = ""
    token: str = ""
    expires_at: datetime = field(default_factory=datetime.utcnow)
    is_revoked: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
