from uuid import UUID
from src.core.services.ride import RideService
from src.handlers.contracts.ride import RideResult
from src.handlers.mappers.ride import RideHandlerMapper


class BoardRideCommandHandler:
    """Admin-only: records the boarding time for an assigned ride."""

    def __init__(self, ride_service: RideService) -> None:
        self.ride_service = ride_service

    async def board_ride(self, rde_id: UUID) -> RideResult:
        entity = await self.ride_service.board(rde_id)
        return RideHandlerMapper.entity_to_result(entity)
