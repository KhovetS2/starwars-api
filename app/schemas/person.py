"""Person schema module."""

from typing import List, Optional
from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    """Base person schema with common attributes."""

    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: List[str] = Field(default_factory=list)
    species: List[str] = Field(default_factory=list)
    vehicles: List[str] = Field(default_factory=list)
    starships: List[str] = Field(default_factory=list)


class PersonResponse(PersonBase):
    """Person response schema."""

    id: int
    url: str
    created: str
    edited: str

    class Config:
        from_attributes = True


class PersonListResponse(BaseModel):
    """Response schema for list of people."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[PersonResponse]


class PersonFilters(BaseModel):
    """Query filters for people."""

    name: Optional[str] = None
