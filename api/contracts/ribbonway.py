from typing import Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class RibbonwayCreateRequest(BaseModel):
    rbn_name: Optional[str] = None
    rbn_description: Optional[str] = None
    rbn_geofence_location: Optional[Any] = None


class RibbonwayUpdateRequest(BaseModel):
    rbn_name: Optional[str] = None
    rbn_description: Optional[str] = None
    rbn_geofence_location: Optional[Any] = None


class RibbonwayResponse(BaseModel):
    rbn_id: UUID
    rbn_created_at: Optional[datetime]
    rbn_name: Optional[str]
    rbn_description: Optional[str]
    rbn_geofence_location: Optional[Any]

    class Config:
        from_attributes = True


class PortalCreateRequest(BaseModel):
    ptl_name: Optional[str] = None
    ptl_description: Optional[str] = None
    ptl_geofence_location: Optional[Any] = None


class PortalResponse(BaseModel):
    ptl_id: UUID
    ptl_created_at: Optional[datetime]
    ptl_name: Optional[str]
    ptl_description: Optional[str]
    ptl_geofence_location: Optional[Any]
    rbn_id: Optional[UUID]

    class Config:
        from_attributes = True


class DockCreateRequest(BaseModel):
    dck_name: Optional[str] = None
    dck_description: Optional[str] = None
    dck_geofence_location: Optional[Any] = None


class DockResponse(BaseModel):
    dck_id: UUID
    dck_created_at: Optional[datetime]
    dck_name: Optional[str]
    dck_description: Optional[str]
    dck_geofence_location: Optional[Any]
    ptl_id: UUID

    class Config:
        from_attributes = True
