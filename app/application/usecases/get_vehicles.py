"""Get vehicles use case module."""

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


class GetVehiclesUseCase:
    """Use case for getting vehicles from SWAPI."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all vehicles with optional filters."""
        data = await self.repository.get_vehicles(search=search, page=page)
        
        # Add ID to each vehicle from URL
        for vehicle in data.get("results", []):
            vehicle["id"] = extract_id_from_url(vehicle.get("url", ""))
        
        return data


class GetVehicleByIdUseCase:
    """Use case for getting a single vehicle by ID."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(self, vehicle_id: int) -> Dict[str, Any]:
        """Get a vehicle by ID."""
        vehicle = await self.repository.get_vehicle_by_id(vehicle_id)
        
        if vehicle is None:
            raise NotFoundError("Vehicle", vehicle_id)
        
        vehicle["id"] = vehicle_id
        return vehicle
