"""Get films use case module."""

from typing import Any, Dict, Optional
import re

from app.infrastructure.repositories.swapi_repository import (
    SwapiRepository,
    get_swapi_repository,
)
from app.domain.errors import NotFoundError


def extract_id_from_url(url: str) -> int:
    """Extract the resource ID from a SWAPI URL."""
    match = re.search(r"/(\d+)/?$", url)
    return int(match.group(1)) if match else 0


class GetFilmsUseCase:
    """Use case for getting films from SWAPI."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all films with optional filters."""
        data = await self.repository.get_films(search=search, page=page)
        
        # Add ID to each film from URL
        for film in data.get("results", []):
            film["id"] = extract_id_from_url(film.get("url", ""))
        
        return data


class GetFilmByIdUseCase:
    """Use case for getting a single film by ID."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(self, film_id: int) -> Dict[str, Any]:
        """Get a film by ID."""
        film = await self.repository.get_film_by_id(film_id)
        
        if film is None:
            raise NotFoundError("Film", film_id)
        
        film["id"] = film_id
        return film
