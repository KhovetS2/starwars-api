"""Pytest configuration and fixtures."""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from app.domain.entities.user import User, RefreshToken


@pytest.fixture
def sample_user() -> User:
    """Sample user for testing."""
    return User(
        id="507f1f77bcf86cd799439011",
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$hashedpassword",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )


@pytest.fixture
def sample_refresh_token() -> RefreshToken:
    """Sample refresh token for testing."""
    return RefreshToken(
        id="507f1f77bcf86cd799439012",
        user_id="507f1f77bcf86cd799439011",
        token="sample_refresh_token_value",
        expires_at=datetime(2024, 12, 31, 23, 59, 59),
        is_revoked=False,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
    )


@pytest.fixture
def sample_film_data() -> dict:
    """Sample film data from SWAPI."""
    return {
        "title": "A New Hope",
        "episode_id": 4,
        "opening_crawl": "It is a period of civil war...",
        "director": "George Lucas",
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1977-05-25",
        "characters": [
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/2/",
        ],
        "planets": ["https://swapi.dev/api/planets/1/"],
        "starships": ["https://swapi.dev/api/starships/2/"],
        "vehicles": ["https://swapi.dev/api/vehicles/4/"],
        "species": ["https://swapi.dev/api/species/1/"],
        "url": "https://swapi.dev/api/films/1/",
        "created": "2014-12-10T14:23:31.880000Z",
        "edited": "2014-12-20T19:49:45.256000Z",
    }


@pytest.fixture
def sample_films_list_data(sample_film_data) -> dict:
    """Sample films list response from SWAPI."""
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [sample_film_data],
    }


@pytest.fixture
def sample_person_data() -> dict:
    """Sample person data from SWAPI."""
    return {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": ["https://swapi.dev/api/films/1/"],
        "species": [],
        "vehicles": ["https://swapi.dev/api/vehicles/14/"],
        "starships": ["https://swapi.dev/api/starships/12/"],
        "url": "https://swapi.dev/api/people/1/",
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z",
    }


@pytest.fixture
def sample_planet_data() -> dict:
    """Sample planet data from SWAPI."""
    return {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": ["https://swapi.dev/api/people/1/"],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/planets/1/",
        "created": "2014-12-09T13:50:49.641000Z",
        "edited": "2014-12-20T20:58:18.411000Z",
    }


@pytest.fixture
def sample_species_data() -> dict:
    """Sample species data from SWAPI."""
    return {
        "name": "Human",
        "classification": "mammal",
        "designation": "sentient",
        "average_height": "180",
        "skin_colors": "caucasian, black, asian, hispanic",
        "hair_colors": "blonde, brown, black, red",
        "eye_colors": "brown, blue, green, hazel, grey, amber",
        "average_lifespan": "120",
        "homeworld": "https://swapi.dev/api/planets/9/",
        "language": "Galactic Basic",
        "people": ["https://swapi.dev/api/people/1/"],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/species/1/",
        "created": "2014-12-10T13:52:11.567000Z",
        "edited": "2014-12-20T21:36:42.136000Z",
    }


@pytest.fixture
def sample_starship_data() -> dict:
    """Sample starship data from SWAPI."""
    return {
        "name": "CR90 corvette",
        "model": "CR90 corvette",
        "manufacturer": "Corellian Engineering Corporation",
        "cost_in_credits": "3500000",
        "length": "150",
        "max_atmosphering_speed": "950",
        "crew": "30-165",
        "passengers": "600",
        "cargo_capacity": "3000000",
        "consumables": "1 year",
        "hyperdrive_rating": "2.0",
        "MGLT": "60",
        "starship_class": "corvette",
        "pilots": [],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/starships/2/",
        "created": "2014-12-10T14:20:33.369000Z",
        "edited": "2014-12-20T21:23:49.867000Z",
    }


@pytest.fixture
def sample_vehicle_data() -> dict:
    """Sample vehicle data from SWAPI."""
    return {
        "name": "Sand Crawler",
        "model": "Digger Crawler",
        "manufacturer": "Corellia Mining Corporation",
        "cost_in_credits": "150000",
        "length": "36.8",
        "max_atmosphering_speed": "30",
        "crew": "46",
        "passengers": "30",
        "cargo_capacity": "50000",
        "consumables": "2 months",
        "vehicle_class": "wheeled",
        "pilots": [],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/vehicles/4/",
        "created": "2014-12-10T15:36:25.724000Z",
        "edited": "2014-12-20T21:30:21.661000Z",
    }


@pytest.fixture
def mock_swapi_repository():
    """Mock SWAPI repository."""
    return AsyncMock()


@pytest.fixture
def mock_user_repository():
    """Mock user repository."""
    return AsyncMock()


@pytest.fixture
def mock_refresh_token_repository():
    """Mock refresh token repository."""
    return AsyncMock()


@pytest.fixture
def mock_auth_service():
    """Mock auth service."""
    mock = MagicMock()
    mock.verify_password = MagicMock(return_value=True)
    mock.hash_password = MagicMock(return_value="$2b$12$hashedpassword")
    mock.create_access_token = MagicMock(return_value="access_token_value")
    mock.create_refresh_token = MagicMock()
    mock.decode_access_token = MagicMock()
    mock.is_refresh_token_valid = MagicMock(return_value=True)
    return mock
