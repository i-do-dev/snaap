from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID


class RideState:
    """Derived ride state — computed from stored timestamps and pod_id (no DB column)"""
    REQUESTED = "requested"
    POD_ASSIGNED = "pod_assigned"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"


@dataclass
class RideRequest:
    """RideRequest domain entity — a rider's journey from boarding to drop-off"""
    rde_id: Optional[UUID] = field(default=None)
    rde_created_at: Optional[datetime] = field(default=None)
    rde_boarding_time: Optional[datetime] = field(default=None)
    rde_dropoff_time: Optional[datetime] = field(default=None)
    rde_amount_charged: Optional[Decimal] = field(default=None)
    rde_currency_charged: Optional[str] = field(default=None)
    rdr_id: Optional[UUID] = field(default=None)
    ptl_id: Optional[UUID] = field(default=None)
    pod_id: Optional[UUID] = field(default=None)
    rde_starting_dock: Optional[UUID] = field(default=None)
    rde_ending_dock: Optional[UUID] = field(default=None)

    @property
    def derived_state(self) -> str:
        """Compute ride state from stored fields — no rde_status column in schema"""
        if self.rde_dropoff_time is not None:
            return RideState.COMPLETED
        if self.rde_boarding_time is not None:
            return RideState.IN_TRANSIT
        if self.pod_id is not None:
            return RideState.POD_ASSIGNED
        return RideState.REQUESTED
