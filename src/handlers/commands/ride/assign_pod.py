from uuid import UUID
from src.core.services.ride import RideService
from src.handlers.contracts.ride import RideAssignCommand, RideResult
from src.handlers.mappers.ride import RideHandlerMapper


class AssignPodCommandHandler:
    """Admin-only: assigns an idle pod to a pending ride request."""

    def __init__(self, ride_service: RideService) -> None:
        self.ride_service = ride_service

    async def assign_pod(self, rde_id: UUID, command: RideAssignCommand) -> RideResult:
        entity = await self.ride_service.assign_pod(rde_id, command.pod_id)
        return RideHandlerMapper.entity_to_result(entity)
