"""Planet schema module."""

from typing import List, Optional
from pydantic import BaseModel, Field


class PlanetBase(BaseModel):
    """Base planet schema with common attributes."""

    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str
    residents: List[str] = Field(default_factory=list)
    films: List[str] = Field(default_factory=list)


class PlanetResponse(PlanetBase):
    """Planet response schema."""

    id: int
    url: str
    created: str
    edited: str

    class Config:
        from_attributes = True


class PlanetListResponse(BaseModel):
    """Response schema for list of planets."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[PlanetResponse]


class PlanetFilters(BaseModel):
    """Query filters for planets."""

    name: Optional[str] = None
    climate: Optional[str] = None
