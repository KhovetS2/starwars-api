"""Vehicles router module."""

from typing import Optional, List, Any, Dict, Literal
from fastapi import APIRouter, HTTPException, status, Query

from app.application.usecases.get_vehicles import GetVehiclesUseCase, GetVehicleByIdUseCase
from app.domain.errors import NotFoundError
from app.schemas.vehicle import VehicleResponse, VehicleListResponse
from app.api.utils.sorting import sort_results


router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

# Fields that should be sorted as numbers
NUMERIC_FIELDS = ["cost_in_credits", "length", "crew", "passengers", "cargo_capacity"]


def filter_vehicles(
    vehicles: List[Dict[str, Any]],
    name: Optional[str] = None,
    model: Optional[str] = None,
    manufacturer: Optional[str] = None,
    vehicle_class: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter vehicles based on criteria."""
    result = vehicles
    
    if name:
        result = [v for v in result if name.lower() in v.get("name", "").lower()]
    
    if model:
        result = [v for v in result if model.lower() in v.get("model", "").lower()]
    
    if manufacturer:
        result = [v for v in result if manufacturer.lower() in v.get("manufacturer", "").lower()]
    
    if vehicle_class:
        result = [v for v in result if vehicle_class.lower() in v.get("vehicle_class", "").lower()]
    
    return result


async def fetch_all_vehicles(use_case: GetVehiclesUseCase, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch all vehicles from SWAPI (handles pagination)."""
    all_vehicles = []
    page = 1
    
    while True:
        data = await use_case.execute(search=search, page=page)
        results = data.get("results", [])
        all_vehicles.extend(results)
        
        if data.get("next") is None:
            break
        page += 1
    
    return all_vehicles


@router.get(
    "/",
    response_model=VehicleListResponse,
    summary="Get all vehicles",
    description="Retrieve a list of all Star Wars vehicles with optional filters.",
)
async def get_all_vehicles(
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    model: Optional[str] = Query(None, description="Filter by model (partial match)"),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer (partial match)"),
    vehicle_class: Optional[str] = Query(None, description="Filter by vehicle class (partial match)"),
    page: Optional[int] = Query(None, ge=1, description="Page number (ignored if model/manufacturer/class filters are active)"),
    sort_by: Optional[Literal["name", "model", "cost_in_credits", "length", "crew", "passengers"]] = Query(None, description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query("asc", description="Sort order: 'asc' or 'desc'"),
):
    """Get all vehicles from SWAPI with optional filters."""
    use_case = GetVehiclesUseCase()
    
    # If model, manufacturer, vehicle_class filters, or sorting is active, fetch all pages
    if model or manufacturer or vehicle_class or sort_by:
        all_vehicles = await fetch_all_vehicles(use_case, search=name)
        filtered = filter_vehicles(all_vehicles, name=name, model=model, manufacturer=manufacturer, vehicle_class=vehicle_class)
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
