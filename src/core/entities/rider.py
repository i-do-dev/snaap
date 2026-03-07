from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.core.value_objects.password import HashedPassword, PlainPassword

if TYPE_CHECKING:
    from src.core.services.password_hasher import IPasswordHasher


@dataclass
class Rider:
    """Rider domain entity — a registered SNAAP passenger"""
    rdr_id: Optional[UUID] = field(default=None)
    rdr_created_at: Optional[datetime] = field(default=None)
    rdr_first_name: Optional[str] = field(default=None)
    rdr_last_name: Optional[str] = field(default=None)
    rdr_email: Optional[str] = field(default=None)
    rdr_phone_number: Optional[str] = field(default=None)
    rdr_avatar: Optional[str] = field(default=None)

    def get_full_name(self) -> str:
        return f"{self.rdr_first_name or ''} {self.rdr_last_name or ''}".strip()


@dataclass
class SecureRider(Rider):
    """Rider entity with password for authentication scenarios"""
    rdr_password: Optional[HashedPassword] = field(default=None)

    def set_password(self, plain_password: PlainPassword, password_hasher: Optional["IPasswordHasher"]) -> None:
        if password_hasher is None:
            raise ValueError("Password hasher is not set")
        self.rdr_password = plain_password.hash_with(password_hasher)

    def authenticate(self, plain_password: PlainPassword, password_hasher: Optional["IPasswordHasher"]) -> bool:
        if self.rdr_password is None or password_hasher is None:
            return False
        return self.rdr_password.verify_against(plain_password.value, password_hasher)
