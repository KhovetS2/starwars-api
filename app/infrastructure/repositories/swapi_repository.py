"""SWAPI repository implementation."""

from typing import Any, Dict, Optional
from app.domain.repositories.swapi_repository import SwapiRepositoryInterface
from app.infrastructure.clients.swapi_client import SwapiClient, get_swapi_client


class SwapiRepository(SwapiRepositoryInterface):
    """SWAPI repository implementation using SWAPI client."""

    def __init__(self, client: Optional[SwapiClient] = None):
        """Initialize repository with SWAPI client."""
        self.client = client or get_swapi_client()

    async def get_films(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all films from SWAPI."""
        return await self.client.get_films(search=search, page=page)

    async def get_film_by_id(self, film_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific film by ID."""
        return await self.client.get_film_by_id(film_id)

    async def get_people(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all people from SWAPI."""
        return await self.client.get_people(search=search, page=page)

    async def get_person_by_id(self, person_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific person by ID."""
        return await self.client.get_person_by_id(person_id)

    async def get_planets(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all planets from SWAPI."""
        return await self.client.get_planets(search=search, page=page)

    async def get_planet_by_id(self, planet_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific planet by ID."""
        return await self.client.get_planet_by_id(planet_id)

    async def get_species(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all species from SWAPI."""
        return await self.client.get_species(search=search, page=page)

    async def get_species_by_id(self, species_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific species by ID."""
        return await self.client.get_species_by_id(species_id)

    async def get_starships(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all starships from SWAPI."""
        return await self.client.get_starships(search=search, page=page)

    async def get_starship_by_id(self, starship_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific starship by ID."""
        return await self.client.get_starship_by_id(starship_id)

    async def get_vehicles(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all vehicles from SWAPI."""
        return await self.client.get_vehicles(search=search, page=page)

    async def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific vehicle by ID."""
        return await self.client.get_vehicle_by_id(vehicle_id)


# Singleton instance
_swapi_repository: Optional[SwapiRepository] = None


def get_swapi_repository() -> SwapiRepository:
    """Get singleton SWAPI repository instance."""
    global _swapi_repository
    if _swapi_repository is None:
        _swapi_repository = SwapiRepository()
    return _swapi_repository
