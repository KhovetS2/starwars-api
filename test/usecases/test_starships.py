"""Test cases for starships use cases."""

import pytest

from app.application.usecases.get_starships import GetStarshipsUseCase, GetStarshipByIdUseCase
from app.domain.errors import NotFoundError


class TestGetStarshipsUseCase:
    """Tests for GetStarshipsUseCase."""

    @pytest.mark.asyncio
    async def test_get_starships_returns_list(
        self, sample_starship_data, mock_swapi_repository
    ):
        """Test getting all starships returns a list."""
        mock_swapi_repository.get_starships.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [sample_starship_data],
        }

        use_case = GetStarshipsUseCase(repository=mock_swapi_repository)
        result = await use_case.execute()

        assert result["count"] == 1
        assert result["results"][0]["name"] == "CR90 corvette"
        assert result["results"][0]["id"] == 2


class TestGetStarshipByIdUseCase:
    """Tests for GetStarshipByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_starship_by_id_success(
        self, sample_starship_data, mock_swapi_repository
    ):
        """Test getting a starship by ID successfully."""
        mock_swapi_repository.get_starship_by_id.return_value = sample_starship_data

        use_case = GetStarshipByIdUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(starship_id=2)

        assert result["name"] == "CR90 corvette"
        assert result["id"] == 2

    @pytest.mark.asyncio
    async def test_get_starship_by_id_not_found(self, mock_swapi_repository):
        """Test getting a starship that doesn't exist raises NotFoundError."""
        mock_swapi_repository.get_starship_by_id.return_value = None

        use_case = GetStarshipByIdUseCase(repository=mock_swapi_repository)

        with pytest.raises(NotFoundError):
            await use_case.execute(starship_id=999)
