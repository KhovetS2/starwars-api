"""Film entity module."""

from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Film:
    """Film entity from SWAPI."""

    id: int
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: date
    characters: List[str]
    planets: List[str]
    starships: List[str]
    vehicles: List[str]
    species: List[str]
    url: str
    created: str
    edited: str
