"""Film schema module."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class FilmBase(BaseModel):
    """Base film schema with common attributes."""

    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: date
    characters: List[str] = Field(default_factory=list)
    planets: List[str] = Field(default_factory=list)
    starships: List[str] = Field(default_factory=list)
    vehicles: List[str] = Field(default_factory=list)
    species: List[str] = Field(default_factory=list)


class FilmResponse(FilmBase):
    """Film response schema."""

    id: int
    url: str
    created: str
    edited: str

    class Config:
        from_attributes = True


class FilmListResponse(BaseModel):
    """Response schema for list of films."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[FilmResponse]


class FilmFilters(BaseModel):
    """Query filters for films."""

    title: Optional[str] = None
    episode_id: Optional[int] = None
