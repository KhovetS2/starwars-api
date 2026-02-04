"""Test cases for species use cases."""

import pytest

from app.application.usecases.get_species import GetSpeciesUseCase, GetSpeciesByIdUseCase
from app.domain.errors import NotFoundError


class TestGetSpeciesUseCase:
    """Tests for GetSpeciesUseCase."""

    @pytest.mark.asyncio
    async def test_get_species_returns_list(
        self, sample_species_data, mock_swapi_repository
    ):
        """Test getting all species returns a list."""
        mock_swapi_repository.get_species.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [sample_species_data],
        }

        use_case = GetSpeciesUseCase(repository=mock_swapi_repository)
        result = await use_case.execute()

        assert result["count"] == 1
        assert result["results"][0]["name"] == "Human"
        assert result["results"][0]["id"] == 1


class TestGetSpeciesByIdUseCase:
    """Tests for GetSpeciesByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_species_by_id_success(
        self, sample_species_data, mock_swapi_repository
    ):
        """Test getting a species by ID successfully."""
        mock_swapi_repository.get_species_by_id.return_value = sample_species_data

        use_case = GetSpeciesByIdUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(species_id=1)

        assert result["name"] == "Human"
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_get_species_by_id_not_found(self, mock_swapi_repository):
        """Test getting a species that doesn't exist raises NotFoundError."""
        mock_swapi_repository.get_species_by_id.return_value = None

        use_case = GetSpeciesByIdUseCase(repository=mock_swapi_repository)

        with pytest.raises(NotFoundError):
            await use_case.execute(species_id=999)
