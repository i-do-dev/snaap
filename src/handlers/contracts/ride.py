from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class RideRequestCommand:
    ptl_id: UUID
    rde_starting_dock: UUID
    rde_ending_dock: UUID


@dataclass(frozen=True)
class RideAssignCommand:
    pod_id: UUID


@dataclass(frozen=True)
class RideCompleteCommand:
    rde_amount_charged: Decimal
    rde_currency_charged: str


@dataclass(frozen=True)
class RideResult:
    rde_id: UUID
    rde_created_at: Optional[datetime]
    rde_boarding_time: Optional[datetime]
    rde_dropoff_time: Optional[datetime]
    rde_amount_charged: Optional[Decimal]
    rde_currency_charged: Optional[str]
    rdr_id: Optional[UUID]
    ptl_id: Optional[UUID]
    pod_id: Optional[UUID]
    rde_starting_dock: Optional[UUID]
    rde_ending_dock: Optional[UUID]
    state: str
