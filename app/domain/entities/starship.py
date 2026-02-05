"""Starship entity module."""

from dataclasses import dataclass
from typing import List


@dataclass
class Starship:
    """Starship entity from SWAPI."""

    id: int
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
    pilots: List[str]
    films: List[str]
    url: str
    created: str
    edited: str
