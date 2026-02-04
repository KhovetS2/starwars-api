"""Starships router module."""

from typing import Optional, List, Any, Dict
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_starships import GetStarshipsUseCase, GetStarshipByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.starship import StarshipResponse, StarshipListResponse


router = APIRouter(prefix="/starships", tags=["Starships"])


def filter_starships(
    starships: List[Dict[str, Any]],
    name: Optional[str] = None,
    model: Optional[str] = None,
    manufacturer: Optional[str] = None,
    starship_class: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter starships based on criteria."""
    result = starships
    
    if name:
        result = [s for s in result if name.lower() in s.get("name", "").lower()]
    
    if model:
        result = [s for s in result if model.lower() in s.get("model", "").lower()]
    
    if manufacturer:
        result = [s for s in result if manufacturer.lower() in s.get("manufacturer", "").lower()]
    
    if starship_class:
        result = [s for s in result if starship_class.lower() in s.get("starship_class", "").lower()]
    
    return result


async def fetch_all_starships(use_case: GetStarshipsUseCase, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch all starships from SWAPI (handles pagination)."""
    all_starships = []
    page = 1
    
    while True:
        data = await use_case.execute(search=search, page=page)
        results = data.get("results", [])
        all_starships.extend(results)
        
        if data.get("next") is None:
            break
        page += 1
    
    return all_starships


@router.get(
    "/",
    response_model=StarshipListResponse,
    summary="Get all starships",
    description="Retrieve a list of all Star Wars starships with optional filters.",
)
async def get_all_starships(
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    model: Optional[str] = Query(None, description="Filter by model (partial match)"),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer (partial match)"),
    starship_class: Optional[str] = Query(None, description="Filter by starship class (partial match)"),
    page: Optional[int] = Query(None, ge=1, description="Page number (ignored if model/manufacturer/class filters are active)"),
):
    """Get all starships from SWAPI with optional filters."""
    use_case = GetStarshipsUseCase()
    
    # If model, manufacturer, or starship_class filters are active, fetch all pages
    if model or manufacturer or starship_class:
        all_starships = await fetch_all_starships(use_case, search=name)
        filtered = filter_starships(all_starships, name=name, model=model, manufacturer=manufacturer, starship_class=starship_class)
        
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
