"""Message use cases module for the spy mini-game."""

from datetime import datetime
from typing import List, Optional

from app.domain.entities.message import EncryptedMessage
from app.domain.entities.user import ForceAlignment
from app.domain.errors import NotFoundError
from app.infrastructure.repositories.message_repository import MessageRepository
from app.application.service.encryption_service import EncryptionService, get_encryption_service


class CreateMessageUseCase:
    """Use case for creating an encrypted message."""

    def __init__(
        self,
        repository: MessageRepository,
        encryption_service: Optional[EncryptionService] = None,
    ):
        """Initialize with dependencies."""
        self.repository = repository
        self.encryption_service = encryption_service or get_encryption_service()

    async def execute(
        self,
        author_id: str,
        text: str,
        alignment: ForceAlignment,
    ) -> EncryptedMessage:
        """Create a message visible to allies and encrypted for enemies.
        
        The message is saved in:
        1. ally_messages collection - with original text visible to allies
        2. enemy_messages collection - with encrypted text for interception by enemies
        """
        now = datetime.utcnow()
        encrypted_text = self.encryption_service.encrypt(text)
        
        # Create ally message (with original text)
        ally_message = EncryptedMessage(
            author_id=author_id,
            original_text=text,
            encrypted_text=encrypted_text,
            alignment=alignment,
            created_at=now,
        )
        await self.repository.create_ally_message(ally_message)
        
        # Create enemy message (same alignment, for interception by the opposite side)
        enemy_message = EncryptedMessage(
            author_id=author_id,
            original_text=text,
            encrypted_text=encrypted_text,
            alignment=alignment,
            created_at=now,
        )
        await self.repository.create_enemy_message(enemy_message)
        
        return ally_message


class GetAllyMessagesUseCase:
    """Use case for getting messages from your side of the Force."""

    def __init__(self, repository: MessageRepository):
        """Initialize with repository."""
        self.repository = repository

    async def execute(
        self,
        alignment: ForceAlignment,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[List[EncryptedMessage], int]:
        """Get all messages from your side with optional sorting."""
        messages = await self.repository.get_ally_messages(
            alignment, skip, limit, sort_by, sort_order
        )
        count = await self.repository.count_ally_messages(alignment)
        return messages, count


class InterceptEnemyMessageUseCase:
    """Use case for intercepting a random enemy message."""

    def __init__(self, repository: MessageRepository):
        """Initialize with repository."""
        self.repository = repository

    async def execute(self, user_alignment: ForceAlignment) -> Optional[EncryptedMessage]:
        """Intercept a random message from the enemy side.
        
        Returns an encrypted message from the opposite alignment.
        The message will only have the encrypted_text visible, not the original.
        """
        message = await self.repository.get_random_enemy_message(user_alignment)
        if message:
            # Clear original text for security - enemy only sees encrypted version
            return EncryptedMessage(
                id=message.id,
                author_id=message.author_id,
                original_text="",  # Hidden from enemy
                encrypted_text=message.encrypted_text,
                alignment=message.alignment,
                created_at=message.created_at,
            )
        return None


class DecryptMessageUseCase:
    """Use case for attempting to decrypt an intercepted message."""

    def __init__(
        self,
        repository: MessageRepository,
        encryption_service: Optional[EncryptionService] = None,
    ):
        """Initialize with dependencies."""
        self.repository = repository
        self.encryption_service = encryption_service or get_encryption_service()

    async def execute(
        self, message_id: str, user_alignment: ForceAlignment
    ) -> tuple[str, bool]:
        """Attempt to decrypt a message.
        
        Returns a tuple of (partial_text, is_complete).
        The partial_text shows revealed letters and underscores for hidden ones.
        
        Reveals between 1/6 and 4/6 of the letters randomly.
        """
        message = await self.repository.get_enemy_message_by_id(message_id)
        
        if message is None:
            raise NotFoundError("Message", message_id)
        
        # Verify user is trying to decrypt enemy message (opposite alignment)
        if message.alignment == user_alignment:
            raise NotFoundError("Message", message_id)  # Can't decrypt your own side's messages
        
        # Partially decrypt using the original text
        partial = self.encryption_service.partial_decrypt(message.original_text)
        
        # Check if complete (no underscores left)
        is_complete = "_" not in partial
        
        return partial, is_complete
