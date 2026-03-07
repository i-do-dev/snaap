from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Ribbonway:
    """Ribbonway domain entity — a physical elevated guideway segment"""
    rbn_id: Optional[UUID] = field(default=None)
    rbn_created_at: Optional[datetime] = field(default=None)
    rbn_name: Optional[str] = field(default=None)
    rbn_description: Optional[str] = field(default=None)
    rbn_geofence_location: Optional[dict] = field(default=None)


@dataclass
class Portal:
    """Portal domain entity — a station/boarding point on a ribbonway"""
    ptl_id: Optional[UUID] = field(default=None)
    ptl_created_at: Optional[datetime] = field(default=None)
    ptl_name: Optional[str] = field(default=None)
    ptl_description: Optional[str] = field(default=None)
    ptl_geofence_location: Optional[dict] = field(default=None)
    rbn_id: Optional[UUID] = field(default=None)


@dataclass
class Dock:
    """Dock domain entity — a docking bay within a portal"""
    dck_id: Optional[UUID] = field(default=None)
    dck_created_at: Optional[datetime] = field(default=None)
    dck_name: Optional[str] = field(default=None)
    dck_description: Optional[str] = field(default=None)
    dck_geofence_location: Optional[dict] = field(default=None)
    ptl_id: Optional[UUID] = field(default=None)
