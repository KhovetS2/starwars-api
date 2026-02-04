"""Get people use case module."""

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


class GetPeopleUseCase:
    """Use case for getting people from SWAPI."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(
        self, search: Optional[str] = None, page: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all people with optional filters."""
        data = await self.repository.get_people(search=search, page=page)
        
        # Add ID to each person from URL
        for person in data.get("results", []):
            person["id"] = extract_id_from_url(person.get("url", ""))
        
        return data


class GetPersonByIdUseCase:
    """Use case for getting a single person by ID."""

    def __init__(self, repository: Optional[SwapiRepository] = None):
        """Initialize with repository."""
        self.repository = repository or get_swapi_repository()

    async def execute(self, person_id: int) -> Dict[str, Any]:
        """Get a person by ID."""
        person = await self.repository.get_person_by_id(person_id)
        
        if person is None:
            raise NotFoundError("Person", person_id)
        
        person["id"] = person_id
        return person
