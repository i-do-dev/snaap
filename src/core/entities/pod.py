from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class PodStatus(str, Enum):
    idle = "idle"
    in_service = "in_service"
    maintenance = "maintenance"
    charging = "charging"
    offline = "offline"


@dataclass
class Pod:
    """Pod domain entity — an individual SNAAP vehicle"""
    pod_id: Optional[UUID] = field(default=None)
    pod_created_at: Optional[datetime] = field(default=None)
    pod_name: Optional[str] = field(default=None)
    pod_description: Optional[str] = field(default=None)
    pod_configuration: Optional[str] = field(default=None)
    pod_current_status: Optional[str] = field(default=PodStatus.idle.value)
    pod_current_location: Optional[str] = field(default=None)
    rbn_id: Optional[UUID] = field(default=None)
