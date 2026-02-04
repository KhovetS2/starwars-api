"""Films router module."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_films import GetFilmsUseCase, GetFilmByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.film import FilmResponse, FilmListResponse


router = APIRouter(prefix="/films", tags=["Films"])


@router.get(
    "/",
    response_model=FilmListResponse,
    summary="Get all films",
    description="Retrieve a list of all Star Wars films with optional search filter.",
)
async def get_all_films(
    search: Optional[str] = Query(None, description="Search by title"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
):
    """Get all films from SWAPI."""
    use_case = GetFilmsUseCase()
    result = await use_case.execute(search=search, page=page)
    return result


@router.get(
    "/{film_id}",
    response_model=FilmResponse,
    summary="Get film by ID",
    description="Retrieve a specific Star Wars film by its ID.",
)
async def get_film_by_id(film_id: int):
    """Get a specific film by ID."""
    use_case = GetFilmByIdUseCase()
    try:
        result = await use_case.execute(film_id)
        return result
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
