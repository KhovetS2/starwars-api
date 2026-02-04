"""Test cases for films use cases."""

import pytest
from unittest.mock import AsyncMock

from app.application.usecases.get_films import GetFilmsUseCase, GetFilmByIdUseCase
from app.domain.errors import NotFoundError


class TestGetFilmsUseCase:
    """Tests for GetFilmsUseCase."""

    @pytest.mark.asyncio
    async def test_get_films_returns_list(
        self, sample_films_list_data, mock_swapi_repository
    ):
        """Test getting all films returns a list."""
        mock_swapi_repository.get_films.return_value = sample_films_list_data

        use_case = GetFilmsUseCase(repository=mock_swapi_repository)
        result = await use_case.execute()

        assert result["count"] == 1
        assert len(result["results"]) == 1
        assert result["results"][0]["title"] == "A New Hope"
        assert result["results"][0]["id"] == 1

    @pytest.mark.asyncio
    async def test_get_films_with_search(
        self, sample_films_list_data, mock_swapi_repository
    ):
        """Test getting films with search parameter."""
        mock_swapi_repository.get_films.return_value = sample_films_list_data

        use_case = GetFilmsUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(search="hope")

        mock_swapi_repository.get_films.assert_called_once_with(search="hope", page=None)
        assert result["count"] == 1

    @pytest.mark.asyncio
    async def test_get_films_with_pagination(
        self, sample_films_list_data, mock_swapi_repository
    ):
        """Test getting films with pagination."""
        mock_swapi_repository.get_films.return_value = sample_films_list_data

        use_case = GetFilmsUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(page=2)

        mock_swapi_repository.get_films.assert_called_once_with(search=None, page=2)


class TestGetFilmByIdUseCase:
    """Tests for GetFilmByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_film_by_id_success(
        self, sample_film_data, mock_swapi_repository
    ):
        """Test getting a film by ID successfully."""
        mock_swapi_repository.get_film_by_id.return_value = sample_film_data

        use_case = GetFilmByIdUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(film_id=1)

        assert result["title"] == "A New Hope"
        assert result["id"] == 1
        mock_swapi_repository.get_film_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_film_by_id_not_found(self, mock_swapi_repository):
        """Test getting a film that doesn't exist raises NotFoundError."""
        mock_swapi_repository.get_film_by_id.return_value = None

        use_case = GetFilmByIdUseCase(repository=mock_swapi_repository)

        with pytest.raises(NotFoundError) as exc_info:
            await use_case.execute(film_id=999)

        assert "Film" in str(exc_info.value.message)
        assert "999" in str(exc_info.value.message)
