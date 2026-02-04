"""People router module."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_people import GetPeopleUseCase, GetPersonByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.person import PersonResponse, PersonListResponse


router = APIRouter(prefix="/people", tags=["People"])


@router.get(
    "/",
    response_model=PersonListResponse,
    summary="Get all people",
    description="Retrieve a list of all Star Wars characters with optional search filter.",
)
async def get_all_people(
    search: Optional[str] = Query(None, description="Search by name"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
):
    """Get all people from SWAPI."""
    use_case = GetPeopleUseCase()
    result = await use_case.execute(search=search, page=page)
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
