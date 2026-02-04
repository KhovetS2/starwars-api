"""Species router module."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_species import GetSpeciesUseCase, GetSpeciesByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.species import SpeciesResponse, SpeciesListResponse


router = APIRouter(prefix="/species", tags=["Species"])


@router.get(
    "/",
    response_model=SpeciesListResponse,
    summary="Get all species",
    description="Retrieve a list of all Star Wars species with optional search filter.",
)
async def get_all_species(
    search: Optional[str] = Query(None, description="Search by name"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
):
    """Get all species from SWAPI."""
    use_case = GetSpeciesUseCase()
    result = await use_case.execute(search=search, page=page)
    return result


@router.get(
    "/{species_id}",
    response_model=SpeciesResponse,
    summary="Get species by ID",
    description="Retrieve a specific Star Wars species by its ID.",
)
async def get_species_by_id(species_id: int):
    """Get a specific species by ID."""
    use_case = GetSpeciesByIdUseCase()
    try:
        result = await use_case.execute(species_id)
        return result
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
