"""Person entity module."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Person:
    """Person entity from SWAPI."""

    id: int
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: List[str]
    species: List[str]
    vehicles: List[str]
    starships: List[str]
    url: str
    created: str
    edited: str
