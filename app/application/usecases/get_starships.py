"""Get starships use case module."""

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


class GetStarshipsUseCase:
    """Use case for getting starships from SWAPI."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all starships with optional filters."""
        data = await self.repository.get_starships(search=search, page=page)
        
        # Add ID to each starship from URL
        for starship in data.get("results", []):
            starship["id"] = extract_id_from_url(starship.get("url", ""))
        
        return data


class GetStarshipByIdUseCase:
    """Use case for getting a single starship by ID."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(self, starship_id: int) -> Dict[str, Any]:
        """Get a starship by ID."""
        starship = await self.repository.get_starship_by_id(starship_id)
        
        if starship is None:
            raise NotFoundError("Starship", starship_id)
        
        starship["id"] = starship_id
        return starship
