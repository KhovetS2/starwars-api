"""User schema module."""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"


class ForceAlignment(str, Enum):
    """Force alignment enumeration."""
    LIGHT = "light"
    DARK = "dark"


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    alignment: ForceAlignment = Field(..., description="Force alignment: 'light' or 'dark'")


class UserCreateAdmin(BaseModel):
    """Schema for creating an admin user (only accessible by admins)."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    alignment: ForceAlignment = Field(..., description="Force alignment: 'light' or 'dark'")


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema for user response."""

    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    role: UserRole = UserRole.USER
    alignment: Optional[ForceAlignment] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Response schema for list of users."""

    count: int
    results: list[UserResponse]
