"""Test cases for message use cases."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from app.application.usecases.message_usecases import (
    CreateMessageUseCase,
    GetAllyMessagesUseCase,
    InterceptEnemyMessageUseCase,
    DecryptMessageUseCase,
)
from app.domain.entities.message import EncryptedMessage
from app.domain.entities.user import ForceAlignment
from app.domain.errors import NotFoundError


@pytest.fixture
def sample_message() -> EncryptedMessage:
    """Sample message for testing."""
    return EncryptedMessage(
        id="507f1f77bcf86cd799439099",
        author_id="507f1f77bcf86cd799439011",
        original_text="The secret base is on Hoth",
        encrypted_text="Gsv hvxivg yzv rh lm Slgs",
        alignment=ForceAlignment.LIGHT,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
    )


@pytest.fixture
def mock_message_repository():
    """Mock message repository."""
    return AsyncMock()


@pytest.fixture
def mock_encryption_service():
    """Mock encryption service."""
    mock = MagicMock()
    mock.encrypt = MagicMock(return_value="encrypted_text_here")
    mock.partial_decrypt = MagicMock(return_value="_h_ __cr__ b_s_ i_ __ H__h")
    return mock


class TestCreateMessageUseCase:
    """Tests for CreateMessageUseCase."""

    @pytest.mark.asyncio
    async def test_create_message_success(
        self, mock_message_repository, mock_encryption_service
    ):
        """Test creating a message successfully."""
        mock_message_repository.create_ally_message.return_value = EncryptedMessage(
            id="new_id",
            author_id="author_123",
            original_text="Secret message",
            encrypted_text="encrypted_text_here",
            alignment=ForceAlignment.LIGHT,
            created_at=datetime.utcnow(),
        )
        mock_message_repository.create_enemy_message.return_value = EncryptedMessage(
            id="enemy_id",
            author_id="author_123",
            original_text="Secret message",
            encrypted_text="encrypted_text_here",
            alignment=ForceAlignment.LIGHT,
            created_at=datetime.utcnow(),
        )

        use_case = CreateMessageUseCase(
            repository=mock_message_repository,
            encryption_service=mock_encryption_service,
        )
        result = await use_case.execute(
            author_id="author_123",
            text="Secret message",
            alignment=ForceAlignment.LIGHT,
        )

        assert result.original_text == "Secret message"
        assert result.alignment == ForceAlignment.LIGHT
        mock_encryption_service.encrypt.assert_called_once_with("Secret message")
        mock_message_repository.create_ally_message.assert_called_once()
        mock_message_repository.create_enemy_message.assert_called_once()


class TestGetAllyMessagesUseCase:
    """Tests for GetAllyMessagesUseCase."""

    @pytest.mark.asyncio
    async def test_get_ally_messages(self, sample_message, mock_message_repository):
        """Test getting ally messages."""
        mock_message_repository.get_ally_messages.return_value = [sample_message]
        mock_message_repository.count_ally_messages.return_value = 1

        use_case = GetAllyMessagesUseCase(repository=mock_message_repository)
        messages, count = await use_case.execute(
            alignment=ForceAlignment.LIGHT, skip=0, limit=10
        )

        assert count == 1
        assert len(messages) == 1
        assert messages[0].original_text == "The secret base is on Hoth"
        mock_message_repository.get_ally_messages.assert_called_once_with(
            ForceAlignment.LIGHT, 0, 10
        )


class TestInterceptEnemyMessageUseCase:
    """Tests for InterceptEnemyMessageUseCase."""

    @pytest.mark.asyncio
    async def test_intercept_enemy_message(self, sample_message, mock_message_repository):
        """Test intercepting an enemy message."""
        mock_message_repository.get_random_enemy_message.return_value = sample_message

        use_case = InterceptEnemyMessageUseCase(repository=mock_message_repository)
        result = await use_case.execute(user_alignment=ForceAlignment.DARK)

        assert result is not None
        assert result.encrypted_text == sample_message.encrypted_text
        # Original text should be hidden
        assert result.original_text == ""
        mock_message_repository.get_random_enemy_message.assert_called_once_with(
            ForceAlignment.DARK
        )

    @pytest.mark.asyncio
    async def test_intercept_no_messages_available(self, mock_message_repository):
        """Test intercepting when no messages are available."""
        mock_message_repository.get_random_enemy_message.return_value = None

        use_case = InterceptEnemyMessageUseCase(repository=mock_message_repository)
        result = await use_case.execute(user_alignment=ForceAlignment.DARK)

        assert result is None


class TestDecryptMessageUseCase:
    """Tests for DecryptMessageUseCase."""

    @pytest.mark.asyncio
    async def test_decrypt_message_partial(
        self, sample_message, mock_message_repository, mock_encryption_service
    ):
        """Test partially decrypting a message."""
        # User is Dark (opposite of message alignment Light)
        mock_message_repository.get_enemy_message_by_id.return_value = sample_message

        use_case = DecryptMessageUseCase(
            repository=mock_message_repository,
            encryption_service=mock_encryption_service,
        )
        partial_text, is_complete = await use_case.execute(
            message_id=sample_message.id,
            user_alignment=ForceAlignment.DARK,
        )

        assert "_" in partial_text  # Should have hidden letters
        assert is_complete is False
        mock_encryption_service.partial_decrypt.assert_called_once_with(
            sample_message.original_text
        )

    @pytest.mark.asyncio
    async def test_decrypt_message_not_found(
        self, mock_message_repository, mock_encryption_service
    ):
        """Test decrypting a message that doesn't exist."""
        mock_message_repository.get_enemy_message_by_id.return_value = None

        use_case = DecryptMessageUseCase(
            repository=mock_message_repository,
            encryption_service=mock_encryption_service,
        )

        with pytest.raises(NotFoundError):
            await use_case.execute(
                message_id="nonexistent",
                user_alignment=ForceAlignment.DARK,
            )

    @pytest.mark.asyncio
    async def test_cannot_decrypt_own_side_message(
        self, sample_message, mock_message_repository, mock_encryption_service
    ):
        """Test that users cannot decrypt messages from their own side."""
        mock_message_repository.get_enemy_message_by_id.return_value = sample_message

        use_case = DecryptMessageUseCase(
            repository=mock_message_repository,
            encryption_service=mock_encryption_service,
        )

        # User is Light, message is also Light -> should fail
        with pytest.raises(NotFoundError):
            await use_case.execute(
                message_id=sample_message.id,
                user_alignment=ForceAlignment.LIGHT,
            )


class TestEncryptionServiceIntegration:
    """Integration tests for encryption service behavior."""

    def test_partial_decrypt_ratio_in_range(self):
        """Test that partial decrypt reveals between 1/6 and 4/6 of letters."""
        from app.application.service.encryption_service import EncryptionService

        service = EncryptionService(seed=42)  # Fixed seed for reproducibility
        text = "The secret base is on Hoth"
        
        letter_count = sum(1 for c in text if c.isalpha())
        
        # Run multiple times to check the range
        for _ in range(10):
            partial = service.partial_decrypt(text)
            revealed_count = sum(1 for c in partial if c.isalpha())
            
            min_expected = max(1, letter_count // 6)
            max_expected = max(min_expected + 1, (letter_count * 4) // 6)
            
            assert min_expected <= revealed_count <= max_expected, \
                f"Revealed {revealed_count} letters, expected between {min_expected} and {max_expected}"

    def test_partial_decrypt_preserves_non_letters(self):
        """Test that spaces and punctuation are preserved."""
        from app.application.service.encryption_service import EncryptionService

        service = EncryptionService(seed=42)
        text = "Hello, World! 123"
        partial = service.partial_decrypt(text)
        
        # Spaces, comma, exclamation mark, and numbers should be preserved
        assert ", " in partial
        assert "! " in partial
        assert "123" in partial
