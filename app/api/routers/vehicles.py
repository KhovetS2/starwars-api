"""Vehicles router module."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_vehicles import GetVehiclesUseCase, GetVehicleByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.vehicle import VehicleResponse, VehicleListResponse


router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get(
    "/",
    response_model=VehicleListResponse,
    summary="Get all vehicles",
    description="Retrieve a list of all Star Wars vehicles with optional search filter.",
)
async def get_all_vehicles(
    search: Optional[str] = Query(None, description="Search by name or model"),
    page: Optional[int] = Query(None, ge=1, description="Page number"),
):
    """Get all vehicles from SWAPI."""
    use_case = GetVehiclesUseCase()
    result = await use_case.execute(search=search, page=page)
    return result


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Get vehicle by ID",
    description="Retrieve a specific Star Wars vehicle by its ID.",
)
async def get_vehicle_by_id(vehicle_id: int):
    """Get a specific vehicle by ID."""
    use_case = GetVehicleByIdUseCase()
    try:
        result = await use_case.execute(vehicle_id)
        return result
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
