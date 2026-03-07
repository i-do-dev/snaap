from typing import Any, Optional, Sequence
from uuid import UUID
from sqlalchemy import select
from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Ribbonway as RibbonwayModel
from src.adapters.db.models import RibbonwayPortal as PortalModel
from src.adapters.db.models import PortalDock as DockModel
from src.core.entities.ribbonway import Ribbonway, Portal, Dock
from src.adapters.db.mappers.ribbonway import RibbonwayMapper, PortalMapper, DockMapper


class RibbonwayRepository(Repository[Ribbonway, RibbonwayModel]):
    model = RibbonwayModel

    async def _model_to_entity(self, model: RibbonwayModel) -> Ribbonway:
        return RibbonwayMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: Ribbonway) -> RibbonwayModel:
        return RibbonwayMapper.entity_to_model(entity)

    async def get(self, rbn_id: UUID) -> Optional[Ribbonway]:
        model = await self.session.get(self.model, rbn_id)
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def delete(self, entity: Ribbonway) -> None:
        model = await self.session.get(self.model, entity.rbn_id)
        if model is None:
            raise ValueError(f"No Ribbonway found with id {entity.rbn_id}")
        await self.session.delete(model)
        await self.session.flush()

    async def update_fields(self, rbn_id: UUID, values: dict[str, Any]) -> Optional[Ribbonway]:
        model = await self.session.get(self.model, rbn_id)
        if model is None:
            return None
        for key, value in values.items():
            if hasattr(model, key):
                setattr(model, key, value)
        await self.session.flush()
        return await self._model_to_entity(model)

    async def has_portals(self, rbn_id: UUID) -> bool:
        statement = select(PortalModel).where(PortalModel.rbn_id == rbn_id).limit(1)
        result = await self.session.execute(statement)
        return result.scalars().first() is not None


class PortalRepository(Repository[Portal, PortalModel]):
    model = PortalModel

    async def _model_to_entity(self, model: PortalModel) -> Portal:
        return PortalMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: Portal) -> PortalModel:
        return PortalMapper.entity_to_model(entity)

    async def get(self, ptl_id: UUID) -> Optional[Portal]:
        model = await self.session.get(self.model, ptl_id)
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def delete(self, entity: Portal) -> None:
        model = await self.session.get(self.model, entity.ptl_id)
        if model is None:
            raise ValueError(f"No Portal found with id {entity.ptl_id}")
        await self.session.delete(model)
        await self.session.flush()

    async def list_by_ribbonway(self, rbn_id: UUID) -> Sequence[Portal]:
        return await self.list(rbn_id=rbn_id)


class DockRepository(Repository[Dock, DockModel]):
    model = DockModel

    async def _model_to_entity(self, model: DockModel) -> Dock:
        return DockMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: Dock) -> DockModel:
        return DockMapper.entity_to_model(entity)

    async def get(self, dck_id: UUID) -> Optional[Dock]:
        model = await self.session.get(self.model, dck_id)
        if model is None:
            return None
        return await self._model_to_entity(model)

    async def delete(self, entity: Dock) -> None:
        model = await self.session.get(self.model, entity.dck_id)
        if model is None:
            raise ValueError(f"No Dock found with id {entity.dck_id}")
        await self.session.delete(model)
        await self.session.flush()

    async def list_by_portal(self, ptl_id: UUID) -> Sequence[Dock]:
        return await self.list(ptl_id=ptl_id)
