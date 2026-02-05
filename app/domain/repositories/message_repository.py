"""Message repository interface module."""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.message import EncryptedMessage
from app.domain.entities.user import ForceAlignment


class MessageRepositoryInterface(ABC):
    """Interface for message repository operations."""

    @abstractmethod
    async def create_ally_message(self, message: EncryptedMessage) -> EncryptedMessage:
        """Create a message in the ally collection."""
        pass

    @abstractmethod
    async def create_enemy_message(self, message: EncryptedMessage) -> EncryptedMessage:
        """Create a message in the enemy collection (for interception)."""
        pass

    @abstractmethod
    async def get_ally_messages(
        self,
        alignment: ForceAlignment,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> List[EncryptedMessage]:
        """Get messages from the ally collection for a specific alignment."""
        pass

    @abstractmethod
    async def get_random_enemy_message(
        self, alignment: ForceAlignment
    ) -> Optional[EncryptedMessage]:
        """Get a random message from the enemy collection for interception."""
        pass

    @abstractmethod
    async def get_enemy_message_by_id(
        self, message_id: str
    ) -> Optional[EncryptedMessage]:
        """Get a specific enemy message by ID."""
        pass

    @abstractmethod
    async def count_ally_messages(self, alignment: ForceAlignment) -> int:
        """Count ally messages for a specific alignment."""
        pass
