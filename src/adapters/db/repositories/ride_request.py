from typing import Any, Optional, Sequence
from uuid import UUID
from sqlalchemy import select
from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import RideRequest as RideRequestModel
from src.core.entities.ride_request import RideRequest
from src.adapters.db.mappers.ride_request import RideRequestMapper


class RideRequestRepository(Repository[RideRequest, RideRequestModel]):
    model = RideRequestModel

    async def _model_to_entity(self, model: RideRequestModel) -> RideRequest:
        return RideRequestMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: RideRequest) -> RideRequestModel:
        return RideRequestMapper.entity_to_model(entity)

    async def get(self, rde_id: UUID) -> Optional[RideRequest]:
        model = await self.session.get(self.model, rde_id)
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def delete(self, entity: RideRequest) -> None:
        model = await self.session.get(self.model, entity.rde_id)
        if model is None:
            raise ValueError(f"No RideRequest found with id {entity.rde_id}")
        await self.session.delete(model)
        await self.session.flush()

    async def update_fields(self, rde_id: UUID, values: dict[str, Any]) -> Optional[RideRequest]:
        model = await self.session.get(self.model, rde_id)
        if model is None:
            return None
        for key, value in values.items():
            if hasattr(model, key):
                setattr(model, key, value)
        await self.session.flush()
        return await self._model_to_entity(model)

    async def list_by_rider(self, rdr_id: UUID, *, offset: int = 0, limit: int = 50) -> Sequence[RideRequest]:
        return await self.list(offset=offset, limit=limit, rdr_id=rdr_id)
