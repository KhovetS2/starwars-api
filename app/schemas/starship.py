"""Starship schema module."""

from typing import List, Optional
from pydantic import BaseModel, Field


class StarshipBase(BaseModel):
    """Base starship schema with common attributes."""

    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str
    starship_class: str
    pilots: List[str] = Field(default_factory=list)
    films: List[str] = Field(default_factory=list)


class StarshipResponse(StarshipBase):
    """Starship response schema."""

    id: int
    url: str
    created: str
    edited: str

    class Config:
        from_attributes = True


class StarshipListResponse(BaseModel):
    """Response schema for list of starships."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[StarshipResponse]


class StarshipFilters(BaseModel):
    """Query filters for starships."""

    name: Optional[str] = None
    model: Optional[str] = None
