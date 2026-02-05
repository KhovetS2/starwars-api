"""People router module."""

from typing import Optional, List, Any, Dict, Literal
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_people import GetPeopleUseCase, GetPersonByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.person import PersonResponse, PersonListResponse
from app.infrastructure.repositories.swapi_repository import get_swapi_repository
from app.api.utils.sorting import sort_results


router = APIRouter(prefix="/people", tags=["People"])


# Cache for species name lookup
_species_cache: Dict[str, str] = {}

# Fields that should be sorted as numbers
NUMERIC_FIELDS = ["height", "mass"]


async def get_species_name(species_url: str) -> str:
    """Get species name from URL with caching."""
    if species_url in _species_cache:
        return _species_cache[species_url]
    
    # Extract species ID from URL
    import re
    match = re.search(r"/species/(\d+)/?$", species_url)
    if not match:
        return ""
    
    species_id = int(match.group(1))
    repo = get_swapi_repository()
    species_data = await repo.get_species_by_id(species_id)
    
    if species_data:
        name = species_data.get("name", "")
        _species_cache[species_url] = name
        return name
    
    return ""


async def filter_people(
    people: List[Dict[str, Any]],
    gender: Optional[str] = None,
    specie: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter people based on criteria."""
    result = people
    
    if gender:
        result = [p for p in result if p.get("gender", "").lower() == gender.lower()]
    
    if specie:
        filtered = []
        for person in result:
            species_urls = person.get("species", [])
            for species_url in species_urls:
                species_name = await get_species_name(species_url)
                if specie.lower() in species_name.lower():
                    filtered.append(person)
                    break
            # Handle humans (empty species list means human)
            if not species_urls and specie.lower() == "human":
                filtered.append(person)
        result = filtered
    
    return result


async def fetch_all_people(use_case: GetPeopleUseCase, name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch all people from SWAPI (handles pagination)."""
    all_people = []
    page = 1
    
    while True:
        data = await use_case.execute(search=name, page=page)
        results = data.get("results", [])
        all_people.extend(results)
        
        if data.get("next") is None:
            break
        page += 1
    
    return all_people


@router.get(
    "/",
    response_model=PersonListResponse,
    summary="Get all people",
    description="Retrieve a list of all Star Wars characters with optional filters.",
)
async def get_all_people(
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    gender: Optional[str] = Query(None, description="Filter by gender (exact match: male, female, n/a, hermaphrodite)"),
    specie: Optional[str] = Query(None, description="Filter by species name (partial match, e.g. 'Human', 'Droid')"),
    page: Optional[int] = Query(None, ge=1, description="Page number (ignored if gender/specie filters are active)"),
    sort_by: Optional[Literal["name", "height", "mass", "birth_year"]] = Query(None, description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query("asc", description="Sort order: 'asc' or 'desc'"),
):
    """Get all people from SWAPI with optional filters."""
    use_case = GetPeopleUseCase()
    
    # If gender, specie filters, or sorting is active, fetch all pages
    if gender or specie or sort_by:
        all_people = await fetch_all_people(use_case, name=name)
        filtered = await filter_people(all_people, gender=gender, specie=specie)
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
    "/{person_id}",
    response_model=PersonResponse,
    summary="Get person by ID",
    description="Retrieve a specific Star Wars character by their ID.",
)
async def get_person_by_id(person_id: int):
    """Get a specific person by ID."""
    use_case = GetPersonByIdUseCase()
    try:
        result = await use_case.execute(person_id)
        return result
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
