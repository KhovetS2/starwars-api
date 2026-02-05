"""Encrypted message entity module."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.domain.entities.user import ForceAlignment


@dataclass
class EncryptedMessage:
    """Encrypted message entity for the spy mini-game."""

    id: Optional[str] = None
    author_id: str = ""
    original_text: str = ""
    encrypted_text: str = ""
    alignment: Optional[ForceAlignment] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
