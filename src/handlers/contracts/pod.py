from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class PodCreateCommand:
    pod_current_location: str
    pod_name: Optional[str] = None
    pod_description: Optional[str] = None
    pod_configuration: Optional[str] = None
    rbn_id: Optional[UUID] = None


@dataclass(frozen=True)
class PodUpdateCommand:
    pod_current_status: Optional[str] = None
    pod_current_location: Optional[str] = None
    rbn_id: Optional[UUID] = None
    pod_name: Optional[str] = None
    pod_description: Optional[str] = None
    pod_configuration: Optional[str] = None


@dataclass(frozen=True)
class PodResult:
    pod_id: UUID
    pod_created_at: Optional[datetime]
    pod_name: Optional[str]
    pod_description: Optional[str]
    pod_configuration: Optional[str]
    pod_current_status: Optional[str]
    pod_current_location: Optional[str]
    rbn_id: Optional[UUID]
