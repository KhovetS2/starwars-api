"""User and RefreshToken repository implementations with MongoDB."""

from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities.user import User, RefreshToken, UserRole, ForceAlignment
from app.domain.repositories.user_repository import (
    UserRepositoryInterface,
    RefreshTokenRepositoryInterface,
)


class UserRepository(UserRepositoryInterface):
    """MongoDB implementation of user repository."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize with database connection."""
        self.db = db
        self.collection = db.users

    def _user_from_doc(self, doc: dict) -> User:
        """Convert MongoDB document to User entity."""
        role_str = doc.get("role", "user")
        alignment_str = doc.get("alignment")
        
        return User(
            id=str(doc["_id"]),
            username=doc["username"],
            email=doc["email"],
            hashed_password=doc["hashed_password"],
            full_name=doc.get("full_name"),
            is_active=doc.get("is_active", True),
            is_superuser=doc.get("is_superuser", False),
            role=UserRole(role_str) if role_str else UserRole.USER,
            alignment=ForceAlignment(alignment_str) if alignment_str else None,
            created_at=doc.get("created_at", datetime.utcnow()),
            updated_at=doc.get("updated_at"),
        )

    def _user_to_doc(self, user: User) -> dict:
        """Convert User entity to MongoDB document."""
        doc = {
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "role": user.role.value if user.role else "user",
            "alignment": user.alignment.value if user.alignment else None,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        if user.id:
            doc["_id"] = ObjectId(user.id)
        return doc

    async def create(self, user: User) -> User:
        """Create a new user."""
        doc = self._user_to_doc(user)
        doc.pop("_id", None)  # Remove _id for insert
        result = await self.collection.insert_one(doc)
        user.id = str(result.inserted_id)
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            return self._user_from_doc(doc) if doc else None
        except Exception:
            return None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        doc = await self.collection.find_one({"username": username})
        return self._user_from_doc(doc) if doc else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        doc = await self.collection.find_one({"email": email})
        return self._user_from_doc(doc) if doc else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        cursor = self.collection.find().skip(skip).limit(limit)
        users = []
        async for doc in cursor:
            users.append(self._user_from_doc(doc))
        return users

    async def update(self, user_id: str, user_data: dict) -> Optional[User]:
        """Update a user."""
        try:
            user_data["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": user_data}
            )
            if result.modified_count > 0:
                return await self.get_by_id(user_id)
            return None
        except Exception:
            return None

    async def delete(self, user_id: str) -> bool:
        """Delete a user."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def count(self) -> int:
        """Count total users."""
        return await self.collection.count_documents({})


class RefreshTokenRepository(RefreshTokenRepositoryInterface):
    """MongoDB implementation of refresh token repository."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize with database connection."""
        self.db = db
        self.collection = db.refresh_tokens

    def _token_from_doc(self, doc: dict) -> RefreshToken:
        """Convert MongoDB document to RefreshToken entity."""
        return RefreshToken(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            token=doc["token"],
            expires_at=doc["expires_at"],
            is_revoked=doc.get("is_revoked", False),
            created_at=doc.get("created_at", datetime.utcnow()),
        )

    def _token_to_doc(self, token: RefreshToken) -> dict:
        """Convert RefreshToken entity to MongoDB document."""
        doc = {
            "user_id": token.user_id,
            "token": token.token,
            "expires_at": token.expires_at,
            "is_revoked": token.is_revoked,
            "created_at": token.created_at,
        }
        if token.id:
            doc["_id"] = ObjectId(token.id)
        return doc

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create a new refresh token."""
        doc = self._token_to_doc(refresh_token)
        doc.pop("_id", None)
        result = await self.collection.insert_one(doc)
        refresh_token.id = str(result.inserted_id)
        return refresh_token

    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get a refresh token by its value."""
        doc = await self.collection.find_one({"token": token})
        return self._token_from_doc(doc) if doc else None

    async def get_by_user_id(self, user_id: str) -> List[RefreshToken]:
        """Get all refresh tokens for a user."""
        cursor = self.collection.find({"user_id": user_id})
        tokens = []
        async for doc in cursor:
            tokens.append(self._token_from_doc(doc))
        return tokens

    async def revoke(self, token: str) -> bool:
        """Revoke a refresh token."""
        result = await self.collection.update_one(
            {"token": token}, {"$set": {"is_revoked": True}}
        )
        return result.modified_count > 0

    async def revoke_all_for_user(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user."""
        result = await self.collection.update_many(
            {"user_id": user_id, "is_revoked": False}, {"$set": {"is_revoked": True}}
        )
        return result.modified_count

    async def delete_expired(self) -> int:
        """Delete all expired tokens."""
        result = await self.collection.delete_many(
            {"expires_at": {"$lt": datetime.utcnow()}}
        )
        return result.deleted_count
