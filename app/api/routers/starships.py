"""Starships router module."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_starships import GetStarshipsUseCase, GetStarshipByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.starship import StarshipResponse, StarshipListResponse


router = APIRouter(prefix="/starships", tags=["Starships"])


@router.get(
    "/",
    response_model=StarshipListResponse,
    summary="Get all starships",
    description="Retrieve a list of all Star Wars starships with optional search filter.",
)
async def get_all_starships(
    search: Optional[str] = Query(None, description="Search by name or model"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
):
    """Get all starships from SWAPI."""
    use_case = GetStarshipsUseCase()
    result = await use_case.execute(search=search, page=page)
    return result


@router.get(
    "/{starship_id}",
    response_model=StarshipResponse,
    summary="Get starship by ID",
    description="Retrieve a specific Star Wars starship by its ID.",
)
async def get_starship_by_id(starship_id: int):
    """Get a specific starship by ID."""
    use_case = GetStarshipByIdUseCase()
    try:
        result = await use_case.execute(starship_id)
        return result
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
