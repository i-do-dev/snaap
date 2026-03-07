from src.core.entities.ribbonway import Ribbonway, Portal, Dock
from src.handlers.contracts.ribbonway import (
    RibbonwayResult, PortalResult, DockResult,
    RibbonwayCreateCommand, PortalCreateCommand, DockCreateCommand,
)


class RibbonwayHandlerMapper:
    @staticmethod
    def entity_to_result(entity: Ribbonway) -> RibbonwayResult:
        return RibbonwayResult(
            rbn_id=entity.rbn_id,
            rbn_created_at=entity.rbn_created_at,
            rbn_name=entity.rbn_name,
            rbn_description=entity.rbn_description,
            rbn_geofence_location=entity.rbn_geofence_location,
        )

    @staticmethod
    def portal_entity_to_result(entity: Portal) -> PortalResult:
        return PortalResult(
            ptl_id=entity.ptl_id,
            ptl_created_at=entity.ptl_created_at,
            ptl_name=entity.ptl_name,
            ptl_description=entity.ptl_description,
            ptl_geofence_location=entity.ptl_geofence_location,
            rbn_id=entity.rbn_id,
        )

    @staticmethod
    def dock_entity_to_result(entity: Dock) -> DockResult:
        return DockResult(
            dck_id=entity.dck_id,
            dck_created_at=entity.dck_created_at,
            dck_name=entity.dck_name,
            dck_description=entity.dck_description,
            dck_geofence_location=entity.dck_geofence_location,
            ptl_id=entity.ptl_id,
        )
