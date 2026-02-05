"""Test cases for vehicles use cases."""

import pytest

from app.application.usecases.get_vehicles import GetVehiclesUseCase, GetVehicleByIdUseCase
from app.domain.errors import NotFoundError


class TestGetVehiclesUseCase:
    """Tests for GetVehiclesUseCase."""

    @pytest.mark.asyncio
    async def test_get_vehicles_returns_list(
        self, sample_vehicle_data, mock_swapi_repository
    ):
        """Test getting all vehicles returns a list."""
        mock_swapi_repository.get_vehicles.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [sample_vehicle_data],
        }

        use_case = GetVehiclesUseCase(repository=mock_swapi_repository)
        result = await use_case.execute()

        assert result["count"] == 1
        assert result["results"][0]["name"] == "Sand Crawler"
        assert result["results"][0]["id"] == 4


class TestGetVehicleByIdUseCase:
    """Tests for GetVehicleByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_vehicle_by_id_success(
        self, sample_vehicle_data, mock_swapi_repository
    ):
        """Test getting a vehicle by ID successfully."""
        mock_swapi_repository.get_vehicle_by_id.return_value = sample_vehicle_data

        use_case = GetVehicleByIdUseCase(repository=mock_swapi_repository)
        result = await use_case.execute(vehicle_id=4)

        assert result["name"] == "Sand Crawler"
        assert result["id"] == 4

    @pytest.mark.asyncio
    async def test_get_vehicle_by_id_not_found(self, mock_swapi_repository):
        """Test getting a vehicle that doesn't exist raises NotFoundError."""
        mock_swapi_repository.get_vehicle_by_id.return_value = None

        use_case = GetVehicleByIdUseCase(repository=mock_swapi_repository)

        with pytest.raises(NotFoundError):
            await use_case.execute(vehicle_id=999)
