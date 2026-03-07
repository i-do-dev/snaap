from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class RiderSignUpCommand:
    rdr_email: str
    rdr_password: str
    rdr_confirm_password: str
    rdr_first_name: Optional[str] = None
    rdr_last_name: Optional[str] = None
    rdr_phone_number: Optional[str] = None


@dataclass(frozen=True)
class RiderSignInResult:
    access_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class RiderProfileResult:
    rdr_id: UUID
    rdr_created_at: Optional[datetime]
    rdr_email: Optional[str]
    rdr_first_name: Optional[str]
    rdr_last_name: Optional[str]
    rdr_phone_number: Optional[str]
    rdr_avatar: Optional[str]


@dataclass(frozen=True)
class RiderUpdateCommand:
    rdr_first_name: Optional[str] = None
    rdr_last_name: Optional[str] = None
    rdr_phone_number: Optional[str] = None
    rdr_avatar: Optional[str] = None
