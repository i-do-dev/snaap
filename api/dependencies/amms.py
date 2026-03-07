"""
AMMS FastAPI dependencies — wires domain handlers to route functions.
"""
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.dependencies.db import Db
from api.dependencies.common import get_token_service
from src.adapters.security.password_hasher import PasswordHasher
from src.adapters.security.token_handler import TokenHandler
from src.core.services.password_hasher import IPasswordHasher
from src.core.services.token_handler import ITokenHandler
from src.handlers.commands.ribbonway.ribbonway_handler import RibbonwayCommandHandler
from src.handlers.commands.pod.pod_handler import PodCommandHandler
from src.handlers.commands.rider.rider_handler import (
    RiderSignUpCommandHandler, RiderSignInCommandHandler,
    RiderProfileQueryHandler, RiderUpdateCommandHandler,
)
from src.handlers.commands.ride.ride_handler import RideRequestCommandHandler
from settings import Settings

# ── Rider OAuth2 scheme (separate from admin/user scheme) ────────────────────
rider_oauth_scheme = OAuth2PasswordBearer(tokenUrl="riders/token")
RiderBearerToken = Annotated[str, Depends(rider_oauth_scheme)]


def get_password_hasher() -> IPasswordHasher:
    return PasswordHasher()


def get_token_handler() -> ITokenHandler:
    return TokenHandler(Settings())


# ── Ribbonway ─────────────────────────────────────────────────────────────────

def get_ribbonway_handler(db: Db) -> RibbonwayCommandHandler:
    return RibbonwayCommandHandler(db)

RibbonwayHandler = Annotated[RibbonwayCommandHandler, Depends(get_ribbonway_handler)]


# ── Pod ───────────────────────────────────────────────────────────────────────

def get_pod_handler(db: Db) -> PodCommandHandler:
    return PodCommandHandler(db)

PodHandler = Annotated[PodCommandHandler, Depends(get_pod_handler)]


# ── Rider ─────────────────────────────────────────────────────────────────────

def get_rider_signup_handler(
    db: Db,
    password_hasher: Annotated[IPasswordHasher, Depends(get_password_hasher)],
) -> RiderSignUpCommandHandler:
    return RiderSignUpCommandHandler(db, password_hasher)

def get_rider_signin_handler(
    db: Db,
    password_hasher: Annotated[IPasswordHasher, Depends(get_password_hasher)],
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)],
) -> RiderSignInCommandHandler:
    return RiderSignInCommandHandler(db, password_hasher, token_handler)

def get_rider_profile_handler(
    db: Db,
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)],
) -> RiderProfileQueryHandler:
    return RiderProfileQueryHandler(db, token_handler)

def get_rider_update_handler(
    db: Db,
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)],
) -> RiderUpdateCommandHandler:
    return RiderUpdateCommandHandler(db, token_handler)

RiderSignupHandlerDep = Annotated[RiderSignUpCommandHandler, Depends(get_rider_signup_handler)]
RiderSigninHandlerDep = Annotated[RiderSignInCommandHandler, Depends(get_rider_signin_handler)]
RiderProfileHandlerDep = Annotated[RiderProfileQueryHandler, Depends(get_rider_profile_handler)]
RiderUpdateHandlerDep = Annotated[RiderUpdateCommandHandler, Depends(get_rider_update_handler)]


# ── Ride ──────────────────────────────────────────────────────────────────────

def get_ride_handler(
    db: Db,
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)],
) -> RideRequestCommandHandler:
    return RideRequestCommandHandler(db, token_handler)

RideHandler = Annotated[RideRequestCommandHandler, Depends(get_ride_handler)]
