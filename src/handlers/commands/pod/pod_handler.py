from typing import Optional, Sequence
from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.pod import Pod, PodStatus
from src.handlers.contracts.pod import PodCreateCommand, PodUpdateCommand, PodResult
from src.handlers.errors import NotFoundError, ConflictError, ValidationError
from src.handlers.mappers.pod import PodHandlerMapper

_VALID_STATUSES = {s.value for s in PodStatus}


class PodCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def create(self, command: PodCreateCommand) -> PodResult:
        entity = Pod(
            pod_name=command.pod_name,
            pod_description=command.pod_description,
            pod_configuration=command.pod_configuration,
            pod_current_status=PodStatus.idle.value,
            pod_current_location=command.pod_current_location,
            rbn_id=command.rbn_id,
        )
        created = await self.db.pod.add(entity)
        return PodHandlerMapper.entity_to_result(created)

    async def list_all(self, offset: int = 0, limit: int = 50,
                       status: Optional[str] = None, rbn_id: Optional[UUID] = None) -> Sequence[PodResult]:
        filters: dict = {}
        if status is not None:
            filters["pod_current_status"] = status
        if rbn_id is not None:
            filters["rbn_id"] = rbn_id
        entities = await self.db.pod.list(offset=offset, limit=limit, **filters)
        return [PodHandlerMapper.entity_to_result(e) for e in entities]

    async def get(self, pod_id: UUID) -> PodResult:
        entity = await self.db.pod.get(pod_id)
        if entity is None:
            raise NotFoundError(f"Pod {pod_id} not found")
        return PodHandlerMapper.entity_to_result(entity)

    async def update(self, pod_id: UUID, command: PodUpdateCommand) -> PodResult:
        if command.pod_current_status and command.pod_current_status not in _VALID_STATUSES:
            raise ValidationError(
                f"Invalid pod status '{command.pod_current_status}'. "
                f"Valid values: {sorted(_VALID_STATUSES)}"
            )
        values = {k: v for k, v in {
            "pod_name": command.pod_name,
            "pod_description": command.pod_description,
            "pod_configuration": command.pod_configuration,
            "pod_current_status": command.pod_current_status,
            "pod_current_location": command.pod_current_location,
            "rbn_id": command.rbn_id,
        }.items() if v is not None}
        entity = await self.db.pod.update_fields(pod_id, values)
        if entity is None:
            raise NotFoundError(f"Pod {pod_id} not found")
        return PodHandlerMapper.entity_to_result(entity)

    async def delete(self, pod_id: UUID) -> None:
        entity = await self.db.pod.get(pod_id)
        if entity is None:
            raise NotFoundError(f"Pod {pod_id} not found")
        if await self.db.pod.has_active_rides(pod_id):
            raise ConflictError("Cannot delete pod with existing ride requests")
        await self.db.pod.delete(entity)
