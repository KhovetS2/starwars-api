"""Authentication service module."""

from datetime import datetime, timedelta
from typing import Optional
import secrets

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.domain.entities.user import User, RefreshToken
from app.schemas.auth import TokenData


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for handling authentication logic."""

    def __init__(self):
        """Initialize auth service."""
        self.settings = get_settings()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    def create_access_token(
        self, user_id: str, username: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {
            "sub": user_id,
            "username": username,
            "exp": expire,
            "type": "access",
        }

        return jwt.encode(
            to_encode,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM,
        )

    def create_refresh_token(self, user_id: str) -> RefreshToken:
        """Create a refresh token."""
        token = secrets.token_urlsafe(64)
        expires_at = datetime.utcnow() + timedelta(
            days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        return RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_revoked=False,
            created_at=datetime.utcnow(),
        )

    def decode_access_token(self, token: str) -> Optional[TokenData]:
        """Decode and validate an access token."""
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM],
            )
            user_id: str = payload.get("sub")
            username: str = payload.get("username")
            token_type: str = payload.get("type")

            if user_id is None or token_type != "access":
                return None

            return TokenData(user_id=user_id, username=username)
        except JWTError:
            return None

    def is_refresh_token_valid(self, refresh_token: RefreshToken) -> bool:
        """Check if a refresh token is valid."""
        if refresh_token.is_revoked:
            return False
        if refresh_token.expires_at < datetime.utcnow():
            return False
        return True


# Singleton instance
_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    """Get singleton auth service instance."""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service
