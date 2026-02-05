"""Species entity module."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Species:
    """Species entity from SWAPI."""

    id: int
    name: str
    classification: str
    designation: str
    average_height: str
    skin_colors: str
    hair_colors: str
    eye_colors: str
    average_lifespan: str
    homeworld: Optional[str]
    language: str
    people: List[str]
    films: List[str]
    url: str
    created: str
    edited: str
