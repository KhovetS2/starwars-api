"""Test cases for auth use cases."""

import pytest
from datetime import datetime, timedelta

from app.application.usecases.auth_usecases import (
    LoginUseCase,
    RefreshTokenUseCase,
    LogoutUseCase,
)
from app.domain.entities.user import RefreshToken
from app.domain.errors import AuthenticationError


class TestLoginUseCase:
    """Tests for LoginUseCase."""

    @pytest.mark.asyncio
    async def test_login_success(
        self,
        sample_user,
        sample_refresh_token,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_auth_service,
    ):
        """Test successful login."""
        mock_user_repository.get_by_username.return_value = sample_user
        mock_auth_service.verify_password.return_value = True
        mock_auth_service.create_access_token.return_value = "access_token"
        mock_auth_service.create_refresh_token.return_value = sample_refresh_token
        mock_refresh_token_repository.create.return_value = sample_refresh_token

        use_case = LoginUseCase(
            user_repository=mock_user_repository,
            token_repository=mock_refresh_token_repository,
            auth_service=mock_auth_service,
        )
        result = await use_case.execute(username="testuser", password="password")

        assert result.access_token == "access_token"
        assert result.refresh_token == sample_refresh_token.token
        assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_username(
        self,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_auth_service,
    ):
        """Test login with invalid username raises AuthenticationError."""
        mock_user_repository.get_by_username.return_value = None

        use_case = LoginUseCase(
            user_repository=mock_user_repository,
            token_repository=mock_refresh_token_repository,
            auth_service=mock_auth_service,
        )

        with pytest.raises(AuthenticationError):
            await use_case.execute(username="invalid", password="password")

    @pytest.mark.asyncio
    async def test_login_invalid_password(
        self,
        sample_user,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_auth_service,
    ):
        """Test login with invalid password raises AuthenticationError."""
        mock_user_repository.get_by_username.return_value = sample_user
        mock_auth_service.verify_password.return_value = False

        use_case = LoginUseCase(
            user_repository=mock_user_repository,
            token_repository=mock_refresh_token_repository,
            auth_service=mock_auth_service,
        )

        with pytest.raises(AuthenticationError):
            await use_case.execute(username="testuser", password="wrongpassword")

    @pytest.mark.asyncio
    async def test_login_inactive_user(
        self,
        sample_user,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_auth_service,
    ):
        """Test login with inactive user raises AuthenticationError."""
        sample_user.is_active = False
        mock_user_repository.get_by_username.return_value = sample_user
        mock_auth_service.verify_password.return_value = True

        use_case = LoginUseCase(
            user_repository=mock_user_repository,
            token_repository=mock_refresh_token_repository,
            auth_service=mock_auth_service,
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await use_case.execute(username="testuser", password="password")

        assert "disabled" in str(exc_info.value.message)


class TestRefreshTokenUseCase:
    """Tests for RefreshTokenUseCase."""

    @pytest.mark.asyncio
    async def test_refresh_token_success(
        self,
        sample_user,
        sample_refresh_token,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_auth_service,
    ):
        """Test refreshing token successfully."""
        new_refresh_token = RefreshToken(
            id="507f1f77bcf86cd799439013",
            user_id=sample_user.id,
            token="new_refresh_token",
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=False,
            created_at=datetime.utcnow(),
        )

        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_auth_service.is_refresh_token_valid.return_value = True
        mock_user_repository.get_by_id.return_value = sample_user
        mock_refresh_token_repository.revoke.return_value = True
        mock_auth_service.create_access_token.return_value = "new_access_token"
        mock_auth_service.create_refresh_token.return_value = new_refresh_token
        mock_refresh_token_repository.create.return_value = new_refresh_token

        use_case = RefreshTokenUseCase(
            user_repository=mock_user_repository,
            token_repository=mock_refresh_token_repository,
            auth_service=mock_auth_service,
        )
        result = await use_case.execute(refresh_token_value=sample_refresh_token.token)

        assert result.access_token == "new_access_token"
        assert result.refresh_token == "new_refresh_token"

    @pytest.mark.asyncio
    async def test_refresh_token_invalid(
        self,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_auth_service,
    ):
        """Test refreshing with invalid token raises AuthenticationError."""
        mock_refresh_token_repository.get_by_token.return_value = None

        use_case = RefreshTokenUseCase(
            user_repository=mock_user_repository,
            token_repository=mock_refresh_token_repository,
            auth_service=mock_auth_service,
        )

        with pytest.raises(AuthenticationError):
            await use_case.execute(refresh_token_value="invalid_token")


class TestLogoutUseCase:
    """Tests for LogoutUseCase."""

    @pytest.mark.asyncio
    async def test_logout_success(self, mock_refresh_token_repository):
        """Test logout revokes all tokens for user."""
        mock_refresh_token_repository.revoke_all_for_user.return_value = 3

        use_case = LogoutUseCase(token_repository=mock_refresh_token_repository)
        result = await use_case.execute(user_id="507f1f77bcf86cd799439011")

        assert result == 3
        mock_refresh_token_repository.revoke_all_for_user.assert_called_once_with(
            "507f1f77bcf86cd799439011"
        )
