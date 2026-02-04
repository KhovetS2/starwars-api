"""Auth schema module."""

from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data payload schema."""

    user_id: str | None = None
    username: str | None = None


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str
