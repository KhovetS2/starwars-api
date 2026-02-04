"""Get planets use case module."""

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


class GetPlanetsUseCase:
    """Use case for getting planets from SWAPI."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all planets with optional filters."""
        data = await self.repository.get_planets(search=search, page=page)
        
        # Add ID to each planet from URL
        for planet in data.get("results", []):
            planet["id"] = extract_id_from_url(planet.get("url", ""))
        
        return data


class GetPlanetByIdUseCase:
    """Use case for getting a single planet by ID."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(self, planet_id: int) -> Dict[str, Any]:
        """Get a planet by ID."""
        planet = await self.repository.get_planet_by_id(planet_id)
        
        if planet is None:
            raise NotFoundError("Planet", planet_id)
        
        planet["id"] = planet_id
        return planet
