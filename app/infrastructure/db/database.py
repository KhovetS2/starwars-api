"""MongoDB database connection module."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from app.core.config import get_settings


class Database:
    """MongoDB database connection manager."""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls) -> None:
        """Connect to MongoDB."""
        settings = get_settings()
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        
        # Create indexes
        await cls._create_indexes()

    @classmethod
    async def disconnect(cls) -> None:
        """Disconnect from MongoDB."""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None

    @classmethod
    async def _create_indexes(cls) -> None:
        """Create database indexes."""
        if cls.db is not None:
            # Users collection indexes
            await cls.db.users.create_index("username", unique=True)
            await cls.db.users.create_index("email", unique=True)
            
            # Refresh tokens collection indexes
            await cls.db.refresh_tokens.create_index("token", unique=True)
            await cls.db.refresh_tokens.create_index("user_id")
            await cls.db.refresh_tokens.create_index("expires_at")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get the database instance."""
        if cls.db is None:
            raise RuntimeError("Database not connected. Call Database.connect() first.")
        return cls.db


def get_database() -> AsyncIOMotorDatabase:
    """Dependency to get database."""
    return Database.get_db()
