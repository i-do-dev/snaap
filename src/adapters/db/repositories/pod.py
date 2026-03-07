from typing import Any, Optional, Sequence
from uuid import UUID
from sqlalchemy import select
from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Pod as PodModel
from src.core.entities.pod import Pod
from src.adapters.db.mappers.pod import PodMapper


class PodRepository(Repository[Pod, PodModel]):
    model = PodModel

    async def _model_to_entity(self, model: PodModel) -> Pod:
        return PodMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: Pod) -> PodModel:
        return PodMapper.entity_to_model(entity)

    async def get(self, pod_id: UUID) -> Optional[Pod]:
        model = await self.session.get(self.model, pod_id)
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def delete(self, entity: Pod) -> None:
        model = await self.session.get(self.model, entity.pod_id)
        if model is None:
            raise ValueError(f"No Pod found with id {entity.pod_id}")
        await self.session.delete(model)
        await self.session.flush()

    async def update_fields(self, pod_id: UUID, values: dict[str, Any]) -> Optional[Pod]:
        model = await self.session.get(self.model, pod_id)
        if model is None:
            return None
        for key, value in values.items():
            if hasattr(model, key):
                setattr(model, key, value)
        await self.session.flush()
        return await self._model_to_entity(model)

    async def has_active_rides(self, pod_id: UUID) -> bool:
        """Check if the pod has any ride requests referencing it"""
        from src.adapters.db.models import RideRequest as RideRequestModel
        statement = select(RideRequestModel).where(RideRequestModel.pod_id == pod_id).limit(1)
        result = await self.session.execute(statement)
        return result.scalars().first() is not None
