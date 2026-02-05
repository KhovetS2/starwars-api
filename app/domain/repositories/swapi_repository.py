"""SWAPI repository interface module."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class SwapiRepositoryInterface(ABC):
    """Abstract interface for SWAPI repository."""

    @abstractmethod
    async def get_films(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all films from SWAPI."""
        pass

    @abstractmethod
    async def get_film_by_id(self, film_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific film by ID."""
        pass

    @abstractmethod
    async def get_people(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all people from SWAPI."""
        pass

    @abstractmethod
    async def get_person_by_id(self, person_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific person by ID."""
        pass

    @abstractmethod
    async def get_planets(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all planets from SWAPI."""
        pass

    @abstractmethod
    async def get_planet_by_id(self, planet_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific planet by ID."""
        pass

    @abstractmethod
    async def get_species(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all species from SWAPI."""
        pass

    @abstractmethod
    async def get_species_by_id(self, species_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific species by ID."""
        pass

    @abstractmethod
    async def get_starships(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all starships from SWAPI."""
        pass

    @abstractmethod
    async def get_starship_by_id(self, starship_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific starship by ID."""
        pass

    @abstractmethod
    async def get_vehicles(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all vehicles from SWAPI."""
        pass

    @abstractmethod
    async def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific vehicle by ID."""
        pass
