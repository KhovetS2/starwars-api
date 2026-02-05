"""Films router module."""

from typing import Optional, List, Any, Dict, Literal
import httpx

from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_films import GetFilmsUseCase, GetFilmByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.film import FilmResponse, FilmListResponse
from app.core.config import get_settings
from app.api.utils.sorting import sort_results


router = APIRouter(prefix="/films", tags=["Films"])

# Cache for character URL -> name mapping
_character_cache: Dict[str, str] = {}

# Fields that should be sorted as numbers
NUMERIC_FIELDS = ["episode_id"]


async def get_character_name(character_url: str) -> str:
    """Fetch character name from URL with caching."""
    if character_url in _character_cache:
        return _character_cache[character_url]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(character_url, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                name = data.get("name", "")
                _character_cache[character_url] = name
                return name
    except Exception:
        pass
    
    return ""


async def filter_films(
    films: List[Dict[str, Any]],
    title: Optional[str] = None,
    director_name: Optional[str] = None,
    producer_name: Optional[str] = None,
    character_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter films based on criteria."""
    result = films
    
    if title:
        result = [f for f in result if title.lower() in f.get("title", "").lower()]
    
    if director_name:
        result = [f for f in result if director_name.lower() in f.get("director", "").lower()]
    
    if producer_name:
        result = [f for f in result if producer_name.lower() in f.get("producer", "").lower()]
    
    if character_name:
        # Filter films by character name (partial match)
        filtered = []
        for film in result:
            character_urls = film.get("characters", [])
            for char_url in character_urls:
                name = await get_character_name(char_url)
                if character_name.lower() in name.lower():
                    filtered.append(film)
                    break
        result = filtered
    
    return result


@router.get(
    "/",
    response_model=FilmListResponse,
    summary="Get all films",
    description="Retrieve a list of all Star Wars films with optional filters.",
)
async def get_all_films(
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    director_name: Optional[str] = Query(None, description="Filter by director name (partial match)"),
    producer_name: Optional[str] = Query(None, description="Filter by producer name (partial match)"),
    character_name: Optional[str] = Query(None, description="Filter by character name present in film (partial match)"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
    sort_by: Optional[Literal["title", "episode_id", "release_date", "director"]] = Query(None, description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query("asc", description="Sort order: 'asc' or 'desc'"),
):
    """Get all films from SWAPI with optional filters."""
    use_case = GetFilmsUseCase()
    
    # Fetch all films (SWAPI has few films, so we fetch all and filter)
    result = await use_case.execute(search=None, page=page)
    
    # Apply filters
    filtered = await filter_films(
        result.get("results", []),
        title=title,
        director_name=director_name,
        producer_name=producer_name,
        character_name=character_name,
    )
    
    # Apply sorting
    sorted_results = sort_results(filtered, sort_by, sort_order, NUMERIC_FIELDS)
    
    return {
        "count": len(sorted_results),
        "next": None,
        "previous": None,
        "results": sorted_results,
    }


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
