"""Planets router module."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_planets import GetPlanetsUseCase, GetPlanetByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.planet import PlanetResponse, PlanetListResponse


router = APIRouter(prefix="/planets", tags=["Planets"])


@router.get(
    "/",
    response_model=PlanetListResponse,
    summary="Get all planets",
    description="Retrieve a list of all Star Wars planets with optional search filter.",
)
async def get_all_planets(
    search: Optional[str] = Query(None, description="Search by name"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
):
    """Get all planets from SWAPI."""
    use_case = GetPlanetsUseCase()
    result = await use_case.execute(search=search, page=page)
    return result


@router.get(
    "/{planet_id}",
    response_model=PlanetResponse,
    summary="Get planet by ID",
    description="Retrieve a specific Star Wars planet by its ID.",
)
async def get_planet_by_id(planet_id: int):
    """Get a specific planet by ID."""
    use_case = GetPlanetByIdUseCase()
    try:
        result = await use_case.execute(planet_id)
        return result
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
