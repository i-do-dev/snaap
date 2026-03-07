from typing import Optional
from uuid import UUID
from sqlalchemy import select
from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Rider as RiderModel
from src.core.entities.rider import Rider, SecureRider
from src.adapters.db.mappers.rider import RiderMapper


class RiderRepository(Repository[Rider, RiderModel]):
    model = RiderModel

    async def _model_to_entity(self, model: RiderModel) -> Rider:
        return RiderMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: SecureRider) -> RiderModel:
        return RiderMapper.entity_to_model(entity)

    async def get(self, rdr_id: UUID) -> Optional[Rider]:
        model = await self.session.get(self.model, rdr_id)
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def get_by_email(self, email: str) -> Optional[Rider]:
        statement = select(self.model).where(self.model.rdr_email == email)
        result = await self.session.execute(statement)
        model = result.scalars().first()
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def get_secure_by_email(self, email: str) -> Optional[SecureRider]:
        statement = select(self.model).where(self.model.rdr_email == email)
        result = await self.session.execute(statement)
        model = result.scalars().first()
        return RiderMapper.model_to_secure_entity(model)

    async def add(self, entity: SecureRider) -> Rider:
        return await super().add(entity)

    async def update_fields(self, rdr_id: UUID, values: dict) -> Optional[Rider]:
        model = await self.session.get(self.model, rdr_id)
        if model is None:
            return None
        for key, value in values.items():
            if hasattr(model, key):
                setattr(model, key, value)
        await self.session.flush()
        return await self._model_to_entity(model)
