"""API routers module."""

from .films import router as films_router
from .people import router as people_router
from .planets import router as planets_router
from .species import router as species_router
from .starships import router as starships_router
from .vehicles import router as vehicles_router
from .auth import router as auth_router
from .user import router as users_router

__all__ = [
    "films_router",
    "people_router",
    "planets_router",
    "species_router",
    "starships_router",
    "vehicles_router",
    "auth_router",
    "users_router",
]
