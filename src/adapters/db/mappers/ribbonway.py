from src.adapters.db.models import Ribbonway as RibbonwayModel
from src.adapters.db.models import RibbonwayPortal as PortalModel
from src.adapters.db.models import PortalDock as DockModel
from src.core.entities.ribbonway import Ribbonway, Portal, Dock


class RibbonwayMapper:
    @staticmethod
    def model_to_entity(model: RibbonwayModel) -> Ribbonway:
        return Ribbonway(
            rbn_id=model.rbn_id,
            rbn_created_at=model.rbn_created_at,
            rbn_name=model.rbn_name,
            rbn_description=model.rbn_description,
            rbn_geofence_location=model.rbn_geofence_location,
        )

    @staticmethod
    def entity_to_model(entity: Ribbonway) -> RibbonwayModel:
        kwargs = {
            "rbn_name": entity.rbn_name,
            "rbn_description": entity.rbn_description,
            "rbn_geofence_location": entity.rbn_geofence_location,
        }
        if entity.rbn_id is not None:
            kwargs["rbn_id"] = entity.rbn_id
        return RibbonwayModel(**kwargs)


class PortalMapper:
    @staticmethod
    def model_to_entity(model: PortalModel) -> Portal:
        return Portal(
            ptl_id=model.ptl_id,
            ptl_created_at=model.ptl_created_at,
            ptl_name=model.ptl_name,
            ptl_description=model.ptl_description,
            ptl_geofence_location=model.ptl_geofence_location,
            rbn_id=model.rbn_id,
        )

    @staticmethod
    def entity_to_model(entity: Portal) -> PortalModel:
        kwargs = {
            "ptl_name": entity.ptl_name,
            "ptl_description": entity.ptl_description,
            "ptl_geofence_location": entity.ptl_geofence_location,
            "rbn_id": entity.rbn_id,
        }
        if entity.ptl_id is not None:
            kwargs["ptl_id"] = entity.ptl_id
        return PortalModel(**kwargs)


class DockMapper:
    @staticmethod
    def model_to_entity(model: DockModel) -> Dock:
        return Dock(
            dck_id=model.dck_id,
            dck_created_at=model.dck_created_at,
            dck_name=model.dck_name,
            dck_description=model.dck_description,
            dck_geofence_location=model.dck_geofence_location,
            ptl_id=model.ptl_id,
        )

    @staticmethod
    def entity_to_model(entity: Dock) -> DockModel:
        kwargs = {
            "dck_name": entity.dck_name,
            "dck_description": entity.dck_description,
            "dck_geofence_location": entity.dck_geofence_location,
            "ptl_id": entity.ptl_id,
        }
        if entity.dck_id is not None:
            kwargs["dck_id"] = entity.dck_id
        return DockModel(**kwargs)
