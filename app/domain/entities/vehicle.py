"""Vehicle entity module."""

from dataclasses import dataclass
from typing import List


@dataclass
class Vehicle:
    """Vehicle entity from SWAPI."""

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
    vehicle_class: str
    pilots: List[str]
    films: List[str]
    url: str
    created: str
    edited: str
