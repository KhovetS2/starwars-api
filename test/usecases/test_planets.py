"""Test cases for planets use cases."""

import pytest

from app.application.usecases.get_planets import GetPlanetsUseCase, GetPlanetByIdUseCase
from app.domain.errors import NotFoundError


class TestGetPlanetsUseCase:
    """Tests for GetPlanetsUseCase."""

    @pytest.mark.asyncio
    async def test_get_planets_returns_list(
        self, sample_planet_data, mock_swapi_repository
    ):
        """Test getting all planets returns a list."""
        mock_swapi_repository.get_planets.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [sample_planet_data],
        }

        use_case = GetPlanetsUseCase(repository=mock_swapi_repository)
        result = await use_case.execute()

        assert result["count"] == 1
        assert result["results"][0]["name"] == "Tatooine"
        assert result["results"][0]["id"] == 1


class TestGetPlanetByIdUseCase:
    """Tests for GetPlanetByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_planet_by_id_success(
        self, sample_planet_data, mock_swapi_repository
    ):
        """Test getting a planet by ID successfully."""
        mock_swapi_repository.get_planet_by_id.return_value = sample_planet_data

        use_case = GetPlanetByIdUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(planet_id=1)

        assert result["name"] == "Tatooine"
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_get_planet_by_id_not_found(self, mock_swapi_repository):
        """Test getting a planet that doesn't exist raises NotFoundError."""
        mock_swapi_repository.get_planet_by_id.return_value = None

        use_case = GetPlanetByIdUseCase(repository=mock_swapi_repository)

        with pytest.raises(NotFoundError):
            await use_case.execute(planet_id=999)
