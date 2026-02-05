"""Test cases for people use cases."""

import pytest
from unittest.mock import AsyncMock

from app.application.usecases.get_people import GetPeopleUseCase, GetPersonByIdUseCase
from app.domain.errors import NotFoundError


class TestGetPeopleUseCase:
    """Tests for GetPeopleUseCase."""

    @pytest.mark.asyncio
    async def test_get_people_returns_list(
        self, sample_person_data, mock_swapi_repository
    ):
        """Test getting all people returns a list."""
        mock_swapi_repository.get_people.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [sample_person_data],
        }

        use_case = GetPeopleUseCase(repository=mock_swapi_repository)
        result = await use_case.execute()

        assert result["count"] == 1
        assert len(result["results"]) == 1
        assert result["results"][0]["name"] == "Luke Skywalker"
        assert result["results"][0]["id"] == 1

    @pytest.mark.asyncio
    async def test_get_people_with_search(
        self, sample_person_data, mock_swapi_repository
    ):
        """Test getting people with search parameter."""
        mock_swapi_repository.get_people.return_value = {
            "count": 1,
            "results": [sample_person_data],
        }

        use_case = GetPeopleUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(search="luke")

        mock_swapi_repository.get_people.assert_called_once_with(search="luke", page=None)


class TestGetPersonByIdUseCase:
    """Tests for GetPersonByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_person_by_id_success(
        self, sample_person_data, mock_swapi_repository
    ):
        """Test getting a person by ID successfully."""
        mock_swapi_repository.get_person_by_id.return_value = sample_person_data

        use_case = GetPersonByIdUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(person_id=1)

        assert result["name"] == "Luke Skywalker"
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_get_person_by_id_not_found(self, mock_swapi_repository):
        """Test getting a person that doesn't exist raises NotFoundError."""
        mock_swapi_repository.get_person_by_id.return_value = None

        use_case = GetPersonByIdUseCase(repository=mock_swapi_repository)

        with pytest.raises(NotFoundError) as exc_info:
            await use_case.execute(person_id=999)

        assert "Person" in str(exc_info.value.message)
