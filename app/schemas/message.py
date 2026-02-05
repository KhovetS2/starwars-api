"""Message schema module."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.schemas.user import ForceAlignment


class MessageCreate(BaseModel):
    """Schema for creating a new encrypted message."""

    text: str = Field(..., min_length=1, max_length=1000, description="Message text to encrypt")


class MessageResponse(BaseModel):
    """Schema for ally message response (with original text visible)."""

    id: str
    author_id: str
    text: str = Field(..., description="Original message text (visible to allies)")
    alignment: ForceAlignment
    created_at: datetime

    class Config:
        from_attributes = True


class EncryptedMessageResponse(BaseModel):
    """Schema for intercepted enemy message (encrypted text only)."""

    id: str
    encrypted_text: str = Field(..., description="Encrypted message text")
    alignment: ForceAlignment
    created_at: datetime

    class Config:
        from_attributes = True


class DecryptAttemptResponse(BaseModel):
    """Schema for decrypt attempt response."""

    partial_text: str = Field(
        ..., 
        description="Partially decrypted text with underscores for hidden letters (e.g., '_a_b_c')"
    )
    is_complete: bool = Field(
        ..., 
        description="True if all letters were revealed"
    )


class MessageListResponse(BaseModel):
    """Response schema for list of ally messages."""

    count: int
    results: List[MessageResponse]
