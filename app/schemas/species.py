"""Species schema module."""

from typing import List, Optional
from pydantic import BaseModel, Field


class SpeciesBase(BaseModel):
    """Base species schema with common attributes."""

    name: str
    classification: str
    designation: str
    average_height: str
    skin_colors: str
    hair_colors: str
    eye_colors: str
    average_lifespan: str
    homeworld: Optional[str] = None
    language: str
    people: List[str] = Field(default_factory=list)
    films: List[str] = Field(default_factory=list)


class SpeciesResponse(SpeciesBase):
    """Species response schema."""

    id: int
    url: str
    created: str
    edited: str

    class Config:
        from_attributes = True


class SpeciesListResponse(BaseModel):
    """Response schema for list of species."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[SpeciesResponse]


class SpeciesFilters(BaseModel):
    """Query filters for species."""

    name: Optional[str] = None
    classification: Optional[str] = None
