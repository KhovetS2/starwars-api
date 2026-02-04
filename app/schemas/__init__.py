"""Schemas module."""

from .film import FilmBase, FilmResponse, FilmListResponse, FilmFilters
from .person import PersonBase, PersonResponse, PersonListResponse, PersonFilters
from .planet import PlanetBase, PlanetResponse, PlanetListResponse, PlanetFilters
from .species import SpeciesBase, SpeciesResponse, SpeciesListResponse, SpeciesFilters
from .starship import StarshipBase, StarshipResponse, StarshipListResponse, StarshipFilters
from .vehicle import VehicleBase, VehicleResponse, VehicleListResponse, VehicleFilters
from .user import UserCreate, UserUpdate, UserResponse, UserListResponse
from .auth import Token, TokenData, LoginRequest, RefreshTokenRequest

__all__ = [
    # Film
    "FilmBase",
    "FilmResponse",
    "FilmListResponse",
    "FilmFilters",
    # Person
    "PersonBase",
    "PersonResponse",
    "PersonListResponse",
    "PersonFilters",
    # Planet
    "PlanetBase",
    "PlanetResponse",
    "PlanetListResponse",
    "PlanetFilters",
    # Species
    "SpeciesBase",
    "SpeciesResponse",
    "SpeciesListResponse",
    "SpeciesFilters",
    # Starship
    "StarshipBase",
    "StarshipResponse",
    "StarshipListResponse",
    "StarshipFilters",
    # Vehicle
    "VehicleBase",
    "VehicleResponse",
    "VehicleListResponse",
    "VehicleFilters",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserListResponse",
    # Auth
    "Token",
    "TokenData",
    "LoginRequest",
    "RefreshTokenRequest",
]
