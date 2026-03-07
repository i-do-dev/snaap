from typing import List, Optional, Sequence
from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.ribbonway import Ribbonway, Portal, Dock
from src.handlers.contracts.ribbonway import (
    RibbonwayCreateCommand, RibbonwayUpdateCommand, RibbonwayResult,
    PortalCreateCommand, PortalResult,
    DockCreateCommand, DockResult,
)
from src.handlers.errors import NotFoundError, ConflictError
from src.handlers.mappers.ribbonway import RibbonwayHandlerMapper


class RibbonwayCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    # ── Ribbonway ─────────────────────────────────────────────────────────────

    async def create(self, command: RibbonwayCreateCommand) -> RibbonwayResult:
        entity = Ribbonway(
            rbn_name=command.rbn_name,
            rbn_description=command.rbn_description,
            rbn_geofence_location=command.rbn_geofence_location,
        )
        created = await self.db.ribbonway.add(entity)
        return RibbonwayHandlerMapper.entity_to_result(created)

    async def list_all(self, offset: int = 0, limit: int = 50) -> Sequence[RibbonwayResult]:
        entities = await self.db.ribbonway.list(offset=offset, limit=limit)
        return [RibbonwayHandlerMapper.entity_to_result(e) for e in entities]

    async def get(self, rbn_id: UUID) -> RibbonwayResult:
        entity = await self.db.ribbonway.get(rbn_id)
        if entity is None:
            raise NotFoundError(f"Ribbonway {rbn_id} not found")
        return RibbonwayHandlerMapper.entity_to_result(entity)

    async def update(self, rbn_id: UUID, command: RibbonwayUpdateCommand) -> RibbonwayResult:
        values = {k: v for k, v in {
            "rbn_name": command.rbn_name,
            "rbn_description": command.rbn_description,
            "rbn_geofence_location": command.rbn_geofence_location,
        }.items() if v is not None}
        entity = await self.db.ribbonway.update_fields(rbn_id, values)
        if entity is None:
            raise NotFoundError(f"Ribbonway {rbn_id} not found")
        return RibbonwayHandlerMapper.entity_to_result(entity)

    async def delete(self, rbn_id: UUID) -> None:
        entity = await self.db.ribbonway.get(rbn_id)
        if entity is None:
            raise NotFoundError(f"Ribbonway {rbn_id} not found")
        if await self.db.ribbonway.has_portals(rbn_id):
            raise ConflictError("Cannot delete ribbonway with existing portals")
        await self.db.ribbonway.delete(entity)

    # ── Portal ────────────────────────────────────────────────────────────────

    async def create_portal(self, command: PortalCreateCommand) -> PortalResult:
        ribbonway = await self.db.ribbonway.get(command.rbn_id)
        if ribbonway is None:
            raise NotFoundError(f"Ribbonway {command.rbn_id} not found")
        entity = Portal(
            rbn_id=command.rbn_id,
            ptl_name=command.ptl_name,
            ptl_description=command.ptl_description,
            ptl_geofence_location=command.ptl_geofence_location,
        )
        created = await self.db.portal.add(entity)
        return RibbonwayHandlerMapper.portal_entity_to_result(created)

    async def list_portals(self, rbn_id: UUID) -> Sequence[PortalResult]:
        entities = await self.db.portal.list_by_ribbonway(rbn_id)
        return [RibbonwayHandlerMapper.portal_entity_to_result(e) for e in entities]

    async def get_portal(self, ptl_id: UUID) -> PortalResult:
        entity = await self.db.portal.get(ptl_id)
        if entity is None:
            raise NotFoundError(f"Portal {ptl_id} not found")
        return RibbonwayHandlerMapper.portal_entity_to_result(entity)

    # ── Dock ──────────────────────────────────────────────────────────────────

    async def create_dock(self, command: DockCreateCommand) -> DockResult:
        portal = await self.db.portal.get(command.ptl_id)
        if portal is None:
            raise NotFoundError(f"Portal {command.ptl_id} not found")
        entity = Dock(
            ptl_id=command.ptl_id,
            dck_name=command.dck_name,
            dck_description=command.dck_description,
            dck_geofence_location=command.dck_geofence_location,
        )
        created = await self.db.dock.add(entity)
        return RibbonwayHandlerMapper.dock_entity_to_result(created)

    async def list_docks(self, ptl_id: UUID) -> Sequence[DockResult]:
        entities = await self.db.dock.list_by_portal(ptl_id)
        return [RibbonwayHandlerMapper.dock_entity_to_result(e) for e in entities]
