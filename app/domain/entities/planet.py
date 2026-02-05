"""Planet entity module."""

from dataclasses import dataclass
from typing import List


@dataclass
class Planet:
    """Planet entity from SWAPI."""

    id: int
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str
    residents: List[str]
    films: List[str]
    url: str
    created: str
    edited: str
