from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import UUID


@dataclass(frozen=True)
class RibbonwayCreateCommand:
    rbn_name: Optional[str] = None
    rbn_description: Optional[str] = None
    rbn_geofence_location: Optional[Any] = None


@dataclass(frozen=True)
class RibbonwayUpdateCommand:
    rbn_name: Optional[str] = None
    rbn_description: Optional[str] = None
    rbn_geofence_location: Optional[Any] = None


@dataclass(frozen=True)
class RibbonwayResult:
    rbn_id: UUID
    rbn_created_at: Optional[datetime]
    rbn_name: Optional[str]
    rbn_description: Optional[str]
    rbn_geofence_location: Optional[Any]


@dataclass(frozen=True)
class PortalCreateCommand:
    rbn_id: UUID
    ptl_name: Optional[str] = None
    ptl_description: Optional[str] = None
    ptl_geofence_location: Optional[Any] = None


@dataclass(frozen=True)
class PortalResult:
    ptl_id: UUID
    ptl_created_at: Optional[datetime]
    ptl_name: Optional[str]
    ptl_description: Optional[str]
    ptl_geofence_location: Optional[Any]
    rbn_id: Optional[UUID]


@dataclass(frozen=True)
class DockCreateCommand:
    ptl_id: UUID
    dck_name: Optional[str] = None
    dck_description: Optional[str] = None
    dck_geofence_location: Optional[Any] = None


@dataclass(frozen=True)
class DockResult:
    dck_id: UUID
    dck_created_at: Optional[datetime]
    dck_name: Optional[str]
    dck_description: Optional[str]
    dck_geofence_location: Optional[Any]
    ptl_id: UUID
