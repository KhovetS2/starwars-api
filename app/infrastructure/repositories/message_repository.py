"""Message repository implementation with MongoDB."""

from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities.message import EncryptedMessage
from app.domain.entities.user import ForceAlignment
from app.domain.repositories.message_repository import MessageRepositoryInterface


class MessageRepository(MessageRepositoryInterface):
    """MongoDB implementation of message repository."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize with database connection."""
        self.db = db
        self.ally_collection = db.ally_messages
        self.enemy_collection = db.enemy_messages

    def _message_from_doc(self, doc: dict) -> EncryptedMessage:
        """Convert MongoDB document to EncryptedMessage entity."""
        alignment_str = doc.get("alignment")
        return EncryptedMessage(
            id=str(doc["_id"]),
            author_id=doc["author_id"],
            original_text=doc.get("original_text", ""),
            encrypted_text=doc.get("encrypted_text", ""),
            alignment=ForceAlignment(alignment_str) if alignment_str else None,
            created_at=doc.get("created_at", datetime.utcnow()),
        )

    def _message_to_doc(self, message: EncryptedMessage) -> dict:
        """Convert EncryptedMessage entity to MongoDB document."""
        doc = {
            "author_id": message.author_id,
            "original_text": message.original_text,
            "encrypted_text": message.encrypted_text,
            "alignment": message.alignment.value if message.alignment else None,
            "created_at": message.created_at,
        }
        if message.id:
            doc["_id"] = ObjectId(message.id)
        return doc

    async def create_ally_message(self, message: EncryptedMessage) -> EncryptedMessage:
        """Create a message in the ally collection."""
        doc = self._message_to_doc(message)
        doc.pop("_id", None)
        result = await self.ally_collection.insert_one(doc)
        message.id = str(result.inserted_id)
        return message

    async def create_enemy_message(self, message: EncryptedMessage) -> EncryptedMessage:
        """Create a message in the enemy collection (for interception)."""
        doc = self._message_to_doc(message)
        doc.pop("_id", None)
        # Enemy collection stores the opposite alignment for interception
        result = await self.enemy_collection.insert_one(doc)
        message.id = str(result.inserted_id)
        return message

    async def get_ally_messages(
        self,
        alignment: ForceAlignment,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> List[EncryptedMessage]:
        """Get messages from the ally collection for a specific alignment."""
        # Convert sort_order to MongoDB direction
        direction = -1 if sort_order == "desc" else 1
        
        cursor = (
            self.ally_collection.find({"alignment": alignment.value})
            .sort(sort_by, direction)
            .skip(skip)
            .limit(limit)
        )
        messages = []
        async for doc in cursor:
            messages.append(self._message_from_doc(doc))
        return messages

    async def get_random_enemy_message(
        self, alignment: ForceAlignment
    ) -> Optional[EncryptedMessage]:
        """Get a random message from the enemy collection for interception.
        
        The alignment parameter is the user's alignment, so we fetch from the
        OPPOSITE alignment (enemy messages).
        """
        opposite = ForceAlignment.DARK if alignment == ForceAlignment.LIGHT else ForceAlignment.LIGHT
        
        # Use MongoDB aggregation to get a random document
        pipeline = [
            {"$match": {"alignment": opposite.value}},
            {"$sample": {"size": 1}},
        ]
        
        cursor = self.enemy_collection.aggregate(pipeline)
        async for doc in cursor:
            return self._message_from_doc(doc)
        return None

    async def get_enemy_message_by_id(
        self, message_id: str
    ) -> Optional[EncryptedMessage]:
        """Get a specific enemy message by ID."""
        try:
            doc = await self.enemy_collection.find_one({"_id": ObjectId(message_id)})
            return self._message_from_doc(doc) if doc else None
        except Exception:
            return None

    async def count_ally_messages(self, alignment: ForceAlignment) -> int:
        """Count ally messages for a specific alignment."""
        return await self.ally_collection.count_documents({"alignment": alignment.value})
