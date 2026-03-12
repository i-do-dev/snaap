from uuid import UUID
from src.core.services.ride import RideService
from src.handlers.contracts.ride import RideCompleteCommand, RideResult
from src.handlers.mappers.ride import RideHandlerMapper


class CompleteRideCommandHandler:
    """Admin-only: marks a ride as completed and records the charge."""

    def __init__(self, ride_service: RideService) -> None:
        self.ride_service = ride_service

    async def complete_ride(self, rde_id: UUID, command: RideCompleteCommand) -> RideResult:
        entity = await self.ride_service.complete(
            rde_id, command.rde_amount_charged, command.rde_currency_charged
        )
        return RideHandlerMapper.entity_to_result(entity)
