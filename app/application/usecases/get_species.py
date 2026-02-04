"""Get species use case module."""

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


class GetSpeciesUseCase:
    """Use case for getting species from SWAPI."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all species with optional filters."""
        data = await self.repository.get_species(search=search, page=page)
        
        # Add ID to each species from URL
        for species in data.get("results", []):
            species["id"] = extract_id_from_url(species.get("url", ""))
        
        return data


class GetSpeciesByIdUseCase:
    """Use case for getting a single species by ID."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(self, species_id: int) -> Dict[str, Any]:
        """Get a species by ID."""
        species = await self.repository.get_species_by_id(species_id)
        
        if species is None:
            raise NotFoundError("Species", species_id)
        
        species["id"] = species_id
        return species
