"""Domain repositories module."""

from .swapi_repository import SwapiRepositoryInterface
from .user_repository import UserRepositoryInterface, RefreshTokenRepositoryInterface

__all__ = [
    "SwapiRepositoryInterface",
    "UserRepositoryInterface",
    "RefreshTokenRepositoryInterface",
]
