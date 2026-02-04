"""SWAPI HTTP client module."""

import httpx
from typing import Any, Dict, Optional
from app.core.config import get_settings


class SwapiClient:
    """HTTP client for consuming SWAPI."""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize SWAPI client."""
        settings = get_settings()
        self.base_url = base_url or settings.SWAPI_BASE_URL
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make a GET request to SWAPI."""
        client = await self._get_client()
        
        # Filter out None params
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = await client.get(endpoint, params=params)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            return None

    # Films
    async def get_films(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all films."""
        result = await self._make_request("/films/", {"search": search, "page": page})
        return result or {"count": 0, "results": []}

    async def get_film_by_id(self, film_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific film by ID."""
        return await self._make_request(f"/films/{film_id}/")

    # People
    async def get_people(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all people."""
        result = await self._make_request("/people/", {"search": search, "page": page})
        return result or {"count": 0, "results": []}

    async def get_person_by_id(self, person_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific person by ID."""
        return await self._make_request(f"/people/{person_id}/")

    # Planets
    async def get_planets(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all planets."""
        result = await self._make_request("/planets/", {"search": search, "page": page})
        return result or {"count": 0, "results": []}

    async def get_planet_by_id(self, planet_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific planet by ID."""
        return await self._make_request(f"/planets/{planet_id}/")

    # Species
    async def get_species(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all species."""
        result = await self._make_request("/species/", {"search": search, "page": page})
        return result or {"count": 0, "results": []}

    async def get_species_by_id(self, species_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific species by ID."""
        return await self._make_request(f"/species/{species_id}/")

    # Starships
    async def get_starships(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all starships."""
        result = await self._make_request("/starships/", {"search": search, "page": page})
        return result or {"count": 0, "results": []}

    async def get_starship_by_id(self, starship_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific starship by ID."""
        return await self._make_request(f"/starships/{starship_id}/")

    # Vehicles
    async def get_vehicles(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all vehicles."""
        result = await self._make_request("/vehicles/", {"search": search, "page": page})
        return result or {"count": 0, "results": []}

    async def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific vehicle by ID."""
        return await self._make_request(f"/vehicles/{vehicle_id}/")


# Singleton instance
_swapi_client: Optional[SwapiClient] = None


def get_swapi_client() -> SwapiClient:
    """Get singleton SWAPI client instance."""
    global _swapi_client
    if _swapi_client is None:
        _swapi_client = SwapiClient()
    return _swapi_client
