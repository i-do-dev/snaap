from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from src.core.entities.pod import PodStatus


class PodCreateRequest(BaseModel):
    pod_current_location: str = Field(..., description="Current location of the pod")
    pod_name: Optional[str] = None
    pod_description: Optional[str] = None
    pod_configuration: Optional[str] = None
    rbn_id: Optional[UUID] = None


class PodUpdateRequest(BaseModel):
    pod_current_status: Optional[str] = None
    pod_current_location: Optional[str] = None
    rbn_id: Optional[UUID] = None
    pod_name: Optional[str] = None
    pod_description: Optional[str] = None
    pod_configuration: Optional[str] = None


class PodResponse(BaseModel):
    pod_id: UUID
    pod_created_at: Optional[datetime]
    pod_name: Optional[str]
    pod_description: Optional[str]
    pod_configuration: Optional[str]
    pod_current_status: Optional[str]
    pod_current_location: Optional[str]
    rbn_id: Optional[UUID]

    class Config:
        from_attributes = True
