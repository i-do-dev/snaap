from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class RideRequestCreate(BaseModel):
    ptl_id: UUID = Field(..., description="Boarding portal UUID")
    rde_starting_dock: UUID = Field(..., description="Starting dock UUID")
    rde_ending_dock: UUID = Field(..., description="Ending dock UUID")


class RideAssignRequest(BaseModel):
    pod_id: UUID


class RideCompleteRequest(BaseModel):
    rde_amount_charged: Decimal
    rde_currency_charged: str = Field(..., min_length=1, max_length=10)


class RideResponse(BaseModel):
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

    class Config:
        from_attributes = True
