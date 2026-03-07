from typing import Optional, Sequence
from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.rider import Rider, SecureRider
from src.core.services.password_hasher import IPasswordHasher
from src.core.services.token_handler import ITokenHandler
from src.core.value_objects.password import PlainPassword
from src.handlers.contracts.rider import (
    RiderSignUpCommand, RiderSignInResult, RiderProfileResult, RiderUpdateCommand,
)
from src.handlers.errors import AuthenticationError, ConflictError, ValidationError
from src.handlers.mappers.rider import RiderHandlerMapper

_INVALID_CREDENTIALS = "Invalid email or password"
_COULD_NOT_VALIDATE = "Could not validate credentials"
_EMAIL_TAKEN = "Email already registered"
_PASSWORDS_NO_MATCH = "Passwords do not match"


class RiderSignUpCommandHandler:
    def __init__(self, db: UnitOfWork, password_hasher: IPasswordHasher) -> None:
        self.db = db
        self.password_hasher = password_hasher

    async def signup(self, command: RiderSignUpCommand) -> RiderProfileResult:
        if command.rdr_password != command.rdr_confirm_password:
            raise ValidationError(_PASSWORDS_NO_MATCH)
        existing = await self.db.rider.get_by_email(command.rdr_email)
        if existing:
            raise ConflictError(_EMAIL_TAKEN)
        rider = SecureRider(
            rdr_first_name=command.rdr_first_name,
            rdr_last_name=command.rdr_last_name,
            rdr_email=command.rdr_email,
            rdr_phone_number=command.rdr_phone_number,
        )
        rider.set_password(PlainPassword(command.rdr_password), self.password_hasher)
        created = await self.db.rider.add(rider)
        return RiderHandlerMapper.entity_to_profile_result(created)


class RiderSignInCommandHandler:
    def __init__(self, db: UnitOfWork, password_hasher: IPasswordHasher, token_handler: ITokenHandler) -> None:
        self.db = db
        self.password_hasher = password_hasher
        self.token_handler = token_handler

    async def sign_in(self, email: str, password: str) -> RiderSignInResult:
        secure_rider = await self.db.rider.get_secure_by_email(email)
        if not secure_rider:
            raise AuthenticationError(_INVALID_CREDENTIALS)
        if not secure_rider.authenticate(PlainPassword(password), self.password_hasher):
            raise AuthenticationError(_INVALID_CREDENTIALS)
        access_token = self.token_handler.create_access_token(data={"sub": email, "type": "rider"})
        return RiderSignInResult(access_token=access_token)


class RiderProfileQueryHandler:
    def __init__(self, db: UnitOfWork, token_handler: ITokenHandler) -> None:
        self.db = db
        self.token_handler = token_handler

    async def get_profile(self, token: str) -> RiderProfileResult:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(_COULD_NOT_VALIDATE) from exc
        rider = await self.db.rider.get_by_email(payload.sub)
        if rider is None:
            raise AuthenticationError(_COULD_NOT_VALIDATE)
        return RiderHandlerMapper.entity_to_profile_result(rider)


class RiderUpdateCommandHandler:
    def __init__(self, db: UnitOfWork, token_handler: ITokenHandler) -> None:
        self.db = db
        self.token_handler = token_handler

    async def update_profile(self, token: str, command: RiderUpdateCommand) -> RiderProfileResult:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(_COULD_NOT_VALIDATE) from exc
        rider = await self.db.rider.get_by_email(payload.sub)
        if rider is None:
            raise AuthenticationError(_COULD_NOT_VALIDATE)
        values = {k: v for k, v in {
            "rdr_first_name": command.rdr_first_name,
            "rdr_last_name": command.rdr_last_name,
            "rdr_phone_number": command.rdr_phone_number,
            "rdr_avatar": command.rdr_avatar,
        }.items() if v is not None}
        updated = await self.db.rider.update_fields(rider.rdr_id, values)
        return RiderHandlerMapper.entity_to_profile_result(updated)
