"""Planets router module."""

from typing import Optional, List, Any, Dict, Literal
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_planets import GetPlanetsUseCase, GetPlanetByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.planet import PlanetResponse, PlanetListResponse
from app.api.utils.sorting import sort_results


router = APIRouter(prefix="/planets", tags=["Planets"])

# Fields that should be sorted as numbers
NUMERIC_FIELDS = ["diameter", "population", "rotation_period", "orbital_period"]


def filter_planets(
    planets: List[Dict[str, Any]],
    name: Optional[str] = None,
    climate: Optional[str] = None,
    terrain: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter planets based on criteria."""
    result = planets
    
    if name:
        result = [p for p in result if name.lower() in p.get("name", "").lower()]
    
    if climate:
        result = [p for p in result if climate.lower() in p.get("climate", "").lower()]
    
    if terrain:
        result = [p for p in result if terrain.lower() in p.get("terrain", "").lower()]
    
    return result


async def fetch_all_planets(use_case: GetPlanetsUseCase, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch all planets from SWAPI (handles pagination)."""
    all_planets = []
    page = 1
    
    while True:
        data = await use_case.execute(search=search, page=page)
        results = data.get("results", [])
        all_planets.extend(results)
        
        if data.get("next") is None:
            break
        page += 1
    
    return all_planets


@router.get(
    "/",
    response_model=PlanetListResponse,
    summary="Get all planets",
    description="Retrieve a list of all Star Wars planets with optional filters.",
)
async def get_all_planets(
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    climate: Optional[str] = Query(None, description="Filter by climate (partial match)"),
    terrain: Optional[str] = Query(None, description="Filter by terrain (partial match)"),
    page: Optional[int] = Query(None, ge=1, description="Page number (ignored if climate/terrain filters are active)"),
    sort_by: Optional[Literal["name", "diameter", "population", "rotation_period", "orbital_period"]] = Query(None, description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query("asc", description="Sort order: 'asc' or 'desc'"),
):
    """Get all planets from SWAPI with optional filters."""
    use_case = GetPlanetsUseCase()
    
    # If climate, terrain filters, or sorting is active, fetch all pages
    if climate or terrain or sort_by:
        all_planets = await fetch_all_planets(use_case, search=name)
        filtered = filter_planets(all_planets, name=name, climate=climate, terrain=terrain)
        sorted_results = sort_results(filtered, sort_by, sort_order, NUMERIC_FIELDS)
        
        return {
            "count": len(sorted_results),
            "next": None,
            "previous": None,
            "results": sorted_results,
        }
    
    # Otherwise, use standard pagination from SWAPI
    result = await use_case.execute(search=name, page=page)
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
