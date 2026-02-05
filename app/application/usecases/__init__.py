"""Application use cases module."""

from .get_films import GetFilmsUseCase, GetFilmByIdUseCase
from .get_people import GetPeopleUseCase, GetPersonByIdUseCase
from .get_planets import GetPlanetsUseCase, GetPlanetByIdUseCase
from .get_species import GetSpeciesUseCase, GetSpeciesByIdUseCase
from .get_starships import GetStarshipsUseCase, GetStarshipByIdUseCase
from .get_vehicles import GetVehiclesUseCase, GetVehicleByIdUseCase
from .user_usecases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from .auth_usecases import LoginUseCase, RefreshTokenUseCase, LogoutUseCase

__all__ = [
    # Films
    "GetFilmsUseCase",
    "GetFilmByIdUseCase",
    # People
    "GetPeopleUseCase",
    "GetPersonByIdUseCase",
    # Planets
    "GetPlanetsUseCase",
    "GetPlanetByIdUseCase",
    # Species
    "GetSpeciesUseCase",
    "GetSpeciesByIdUseCase",
    # Starships
    "GetStarshipsUseCase",
    "GetStarshipByIdUseCase",
    # Vehicles
    "GetVehiclesUseCase",
    "GetVehicleByIdUseCase",
    # Users
    "CreateUserUseCase",
    "GetUserByIdUseCase",
    "GetAllUsersUseCase",
    "UpdateUserUseCase",
    "DeleteUserUseCase",
    # Auth
    "LoginUseCase",
    "RefreshTokenUseCase",
    "LogoutUseCase",
]
