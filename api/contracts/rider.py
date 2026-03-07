from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class RiderRegisterRequest(BaseModel):
    rdr_email: EmailStr
    rdr_password: str = Field(..., min_length=8)
    rdr_confirm_password: str = Field(..., min_length=8)
    rdr_first_name: Optional[str] = None
    rdr_last_name: Optional[str] = None
    rdr_phone_number: Optional[str] = None


class RiderUpdateRequest(BaseModel):
    rdr_first_name: Optional[str] = None
    rdr_last_name: Optional[str] = None
    rdr_phone_number: Optional[str] = None
    rdr_avatar: Optional[str] = None


class RiderProfileResponse(BaseModel):
    rdr_id: UUID
    rdr_created_at: Optional[datetime]
    rdr_email: Optional[str]
    rdr_first_name: Optional[str]
    rdr_last_name: Optional[str]
    rdr_phone_number: Optional[str]
    rdr_avatar: Optional[str]

    class Config:
        from_attributes = True
