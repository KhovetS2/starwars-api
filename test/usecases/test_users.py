"""Test cases for user use cases."""

import pytest
from datetime import datetime

from app.application.usecases.user_usecases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from app.domain.entities.user import User, UserRole, ForceAlignment
from app.domain.errors import NotFoundError, DuplicateError


class TestCreateUserUseCase:
    """Tests for CreateUserUseCase."""

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, mock_user_repository, mock_auth_service
    ):
        """Test creating a user successfully."""
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.create.return_value = User(
            id="507f1f77bcf86cd799439011",
            username="newuser",
            email="new@example.com",
            hashed_password="$2b$12$hashedpassword",
            full_name="New User",
            is_active=True,
            is_superuser=False,
            role=UserRole.USER,
            alignment=ForceAlignment.LIGHT,
            created_at=datetime.utcnow(),
        )

        use_case = CreateUserUseCase(
            repository=mock_user_repository,
            auth_service=mock_auth_service,
        )
        result = await use_case.execute(
            username="newuser",
            email="new@example.com",
            password="password123",
            alignment=ForceAlignment.LIGHT,
            full_name="New User",
        )

        assert result.username == "newuser"
        assert result.email == "new@example.com"
        assert result.alignment == ForceAlignment.LIGHT
        mock_auth_service.hash_password.assert_called_once_with("password123")

    @pytest.mark.asyncio
    async def test_create_user_duplicate_username(
        self, sample_user, mock_user_repository, mock_auth_service
    ):
        """Test creating a user with duplicate username raises DuplicateError."""
        mock_user_repository.get_by_username.return_value = sample_user

        use_case = CreateUserUseCase(
            repository=mock_user_repository,
            auth_service=mock_auth_service,
        )

        with pytest.raises(DuplicateError) as exc_info:
            await use_case.execute(
                username="testuser",
                email="new@example.com",
                password="password123",
                alignment=ForceAlignment.DARK,
            )

        assert "username" in str(exc_info.value.message)


class TestGetUserByIdUseCase:
    """Tests for GetUserByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(
        self, sample_user, mock_user_repository
    ):
        """Test getting a user by ID successfully."""
        mock_user_repository.get_by_id.return_value = sample_user

        use_case = GetUserByIdUseCase(repository=mock_user_repository)
        result = await use_case.execute(user_id=sample_user.id)

        assert result.username == "testuser"

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, mock_user_repository):
        """Test getting a user that doesn't exist raises NotFoundError."""
        mock_user_repository.get_by_id.return_value = None

        use_case = GetUserByIdUseCase(repository=mock_user_repository)

        with pytest.raises(NotFoundError):
            await use_case.execute(user_id="nonexistent")


class TestGetAllUsersUseCase:
    """Tests for GetAllUsersUseCase."""

    @pytest.mark.asyncio
    async def test_get_all_users(self, sample_user, mock_user_repository):
        """Test getting all users."""
        mock_user_repository.get_all.return_value = [sample_user]
        mock_user_repository.count.return_value = 1

        use_case = GetAllUsersUseCase(repository=mock_user_repository)
        users, count = await use_case.execute()

        assert count == 1
        assert len(users) == 1
        assert users[0].username == "testuser"


class TestUpdateUserUseCase:
    """Tests for UpdateUserUseCase."""

    @pytest.mark.asyncio
    async def test_update_user_success(
        self, sample_user, mock_user_repository, mock_auth_service
    ):
        """Test updating a user successfully."""
        mock_user_repository.get_by_id.return_value = sample_user
        mock_user_repository.get_by_username.return_value = None
        
        updated_user = User(
            id=sample_user.id,
            username="updateduser",
            email=sample_user.email,
            hashed_password=sample_user.hashed_password,
            full_name="Updated Name",
            is_active=True,
            is_superuser=False,
            alignment=sample_user.alignment,
            created_at=sample_user.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(
            repository=mock_user_repository,
            auth_service=mock_auth_service,
        )
        result = await use_case.execute(
            user_id=sample_user.id,
            username="updateduser",
            full_name="Updated Name",
        )

        assert result.username == "updateduser"
        assert result.full_name == "Updated Name"

    @pytest.mark.asyncio
    async def test_update_user_alignment(
        self, sample_user, mock_user_repository, mock_auth_service
    ):
        """Test updating user alignment (changing side of the Force)."""
        mock_user_repository.get_by_id.return_value = sample_user
        
        updated_user = User(
            id=sample_user.id,
            username=sample_user.username,
            email=sample_user.email,
            hashed_password=sample_user.hashed_password,
            full_name=sample_user.full_name,
            is_active=True,
            is_superuser=False,
            alignment=ForceAlignment.DARK,  # Changed from LIGHT to DARK
            created_at=sample_user.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(
            repository=mock_user_repository,
            auth_service=mock_auth_service,
        )
        result = await use_case.execute(
            user_id=sample_user.id,
            alignment=ForceAlignment.DARK,
        )

        assert result.alignment == ForceAlignment.DARK


class TestDeleteUserUseCase:
    """Tests for DeleteUserUseCase."""

    @pytest.mark.asyncio
    async def test_delete_user_success(self, sample_user, mock_user_repository):
        """Test deleting a user successfully."""
        mock_user_repository.get_by_id.return_value = sample_user
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(repository=mock_user_repository)
        result = await use_case.execute(user_id=sample_user.id)

        assert result is True

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, mock_user_repository):
        """Test deleting a user that doesn't exist raises NotFoundError."""
        mock_user_repository.get_by_id.return_value = None

        use_case = DeleteUserUseCase(repository=mock_user_repository)

        with pytest.raises(NotFoundError):
            await use_case.execute(user_id="nonexistent")
