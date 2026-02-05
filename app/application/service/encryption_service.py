"""Encryption service for the spy mini-game."""

import random
import string


class EncryptionService:
    """Service for encrypting and partially decrypting messages."""

    def __init__(self, seed: int = None):
        """Initialize with optional seed for testing."""
        self._random = random.Random(seed)

    def encrypt(self, text: str) -> str:
        """Encrypt text using a simple substitution cipher.
        
        This creates a randomized substitution where each letter maps to another.
        Non-letter characters remain unchanged.
        """
        # Create a random substitution alphabet
        alphabet = list(string.ascii_lowercase)
        shuffled = alphabet.copy()
        self._random.shuffle(shuffled)
        
        # Create mapping
        encrypt_map = dict(zip(alphabet, shuffled))
        encrypt_map_upper = {k.upper(): v.upper() for k, v in encrypt_map.items()}
        encrypt_map.update(encrypt_map_upper)
        
        # Encrypt
        result = []
        for char in text:
            if char in encrypt_map:
                result.append(encrypt_map[char])
            else:
                result.append(char)
        
        return "".join(result)

    def partial_decrypt(self, original_text: str) -> str:
        """Partially decrypt a message, revealing between 1/6 and 4/6 of the letters.
        
        Returns a string in the format "_a_b_c" where underscores represent
        hidden letters and actual letters are revealed.
        Non-letter characters (spaces, punctuation) are always shown.
        """
        # Count letters only (not spaces/punctuation)
        letters_count = sum(1 for c in original_text if c.isalpha())
        
        if letters_count == 0:
            return original_text
        
        # Calculate how many letters to reveal (between 1/6 and 4/6)
        min_reveal = max(1, letters_count // 6)
        max_reveal = max(min_reveal + 1, (letters_count * 4) // 6)
        reveal_count = self._random.randint(min_reveal, max_reveal)
        
        # Get indices of all letters
        letter_indices = [i for i, c in enumerate(original_text) if c.isalpha()]
        
        # Randomly select which letters to reveal
        reveal_indices = set(self._random.sample(letter_indices, min(reveal_count, len(letter_indices))))
        
        # Build result
        result = []
        for i, char in enumerate(original_text):
            if char.isalpha():
                if i in reveal_indices:
                    result.append(char)
                else:
                    result.append("_")
            else:
                # Keep spaces, punctuation, etc.
                result.append(char)
        
        return "".join(result)


# Singleton instance
_encryption_service = None


def get_encryption_service() -> EncryptionService:
    """Get the encryption service singleton."""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service
