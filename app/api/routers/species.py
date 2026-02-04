"""Species router module."""

from typing import Optional, List, Any, Dict
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_species import GetSpeciesUseCase, GetSpeciesByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.species import SpeciesResponse, SpeciesListResponse


router = APIRouter(prefix="/species", tags=["Species"])


def filter_species(
    species_list: List[Dict[str, Any]],
    name: Optional[str] = None,
    classification: Optional[str] = None,
    language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter species based on criteria."""
    result = species_list
    
    if name:
        result = [s for s in result if name.lower() in s.get("name", "").lower()]
    
    if classification:
        result = [s for s in result if classification.lower() in s.get("classification", "").lower()]
    
    if language:
        result = [s for s in result if language.lower() in s.get("language", "").lower()]
    
    return result


async def fetch_all_species(use_case: GetSpeciesUseCase, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch all species from SWAPI (handles pagination)."""
    all_species = []
    page = 1
    
    while True:
        data = await use_case.execute(search=search, page=page)
        results = data.get("results", [])
        all_species.extend(results)
        
        if data.get("next") is None:
            break
        page += 1
    
    return all_species


@router.get(
    "/",
    response_model=SpeciesListResponse,
    summary="Get all species",
    description="Retrieve a list of all Star Wars species with optional filters.",
)
async def get_all_species(
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    classification: Optional[str] = Query(None, description="Filter by classification (partial match, e.g. 'mammal', 'reptile')"),
    language: Optional[str] = Query(None, description="Filter by language (partial match)"),
    page: Optional[int] = Query(None, ge=1, description="Page number (ignored if classification/language filters are active)"),
):
    """Get all species from SWAPI with optional filters."""
    use_case = GetSpeciesUseCase()
    
    # If classification or language filters are active, fetch all pages
    if classification or language:
        all_species = await fetch_all_species(use_case, search=name)
        filtered = filter_species(all_species, name=name, classification=classification, language=language)
        
        return {
            "count": len(filtered),
            "next": None,
            "previous": None,
            "results": filtered,
        }
    
    # Otherwise, use standard pagination from SWAPI
    result = await use_case.execute(search=name, page=page)
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
