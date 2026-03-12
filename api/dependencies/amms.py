"""
AMMS FastAPI dependencies — wires domain handlers to route functions.

Auth split:
  - Rider endpoints  → Supabase JWT (SupabaseTokenHandler, tokenUrl="riders/token")
  - Admin endpoints  → Custom JWT  (TokenHandler, tokenUrl="auth/token")
"""
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.dependencies.db import Db
from src.adapters.security.supabase_token_handler import SupabaseTokenHandler
from src.adapters.security.token_handler import TokenHandler
from src.core.services.token_handler import ITokenHandler
from src.core.services.rider import RiderService
from src.core.services.ride import RideService
from src.handlers.commands.ribbonway.ribbonway_handler import RibbonwayCommandHandler
from src.handlers.commands.pod.pod_handler import PodCommandHandler
from src.handlers.commands.rider.update_rider_profile import UpdateRiderProfileCommandHandler
from src.handlers.commands.ride.request_ride import RequestRideCommandHandler
from src.handlers.commands.ride.assign_pod import AssignPodCommandHandler
from src.handlers.commands.ride.board_ride import BoardRideCommandHandler
from src.handlers.commands.ride.complete_ride import CompleteRideCommandHandler
from src.handlers.commands.ride.cancel_ride import CancelRideCommandHandler
from src.handlers.queries.rider.get_rider_profile import GetRiderProfileQueryHandler
from src.handlers.queries.ride.get_ride import GetRideQueryHandler
from src.handlers.queries.ride.list_my_rides import ListMyRidesQueryHandler
from settings import Settings

# ── Rider OAuth2 scheme — tokenUrl is informational for Swagger UI only.
# Riders authenticate via Supabase; they obtain tokens from the Supabase project,
# not from this backend.  The bearer token sent here is a Supabase-issued JWT.
rider_oauth_scheme = OAuth2PasswordBearer(tokenUrl="riders/token")
RiderBearerToken = Annotated[str, Depends(rider_oauth_scheme)]


def get_supabase_token_handler() -> SupabaseTokenHandler:
    return SupabaseTokenHandler(Settings())


def get_token_handler() -> ITokenHandler:
    return TokenHandler(Settings())


# ── Domain services ───────────────────────────────────────────────────────────

def get_rider_service(db: Db) -> RiderService:
    return RiderService(db)

def get_ride_service(db: Db) -> RideService:
    return RideService(db)

RiderServiceDep = Annotated[RiderService, Depends(get_rider_service)]
RideServiceDep = Annotated[RideService, Depends(get_ride_service)]


# ── Ribbonway ─────────────────────────────────────────────────────────────────

def get_ribbonway_handler(db: Db) -> RibbonwayCommandHandler:
    return RibbonwayCommandHandler(db)

RibbonwayHandler = Annotated[RibbonwayCommandHandler, Depends(get_ribbonway_handler)]


# ── Pod ───────────────────────────────────────────────────────────────────────

def get_pod_handler(db: Db) -> PodCommandHandler:
    return PodCommandHandler(db)

PodHandler = Annotated[PodCommandHandler, Depends(get_pod_handler)]


# ── Rider queries and commands ────────────────────────────────────────────────

def get_rider_profile_handler(
    rider_service: RiderServiceDep,
    token_handler: Annotated[SupabaseTokenHandler, Depends(get_supabase_token_handler)],
) -> GetRiderProfileQueryHandler:
    return GetRiderProfileQueryHandler(rider_service, token_handler)

def get_update_rider_profile_handler(
    rider_service: RiderServiceDep,
    token_handler: Annotated[SupabaseTokenHandler, Depends(get_supabase_token_handler)],
) -> UpdateRiderProfileCommandHandler:
    return UpdateRiderProfileCommandHandler(rider_service, token_handler)

GetRiderProfileHandlerDep = Annotated[GetRiderProfileQueryHandler, Depends(get_rider_profile_handler)]
UpdateRiderProfileHandlerDep = Annotated[UpdateRiderProfileCommandHandler, Depends(get_update_rider_profile_handler)]


# ── Ride queries ──────────────────────────────────────────────────────────────

def get_ride_query_handler(
    ride_service: RideServiceDep,
    rider_service: RiderServiceDep,
    token_handler: Annotated[SupabaseTokenHandler, Depends(get_supabase_token_handler)],
) -> GetRideQueryHandler:
    return GetRideQueryHandler(ride_service, rider_service, token_handler)

def get_list_my_rides_handler(
    ride_service: RideServiceDep,
    rider_service: RiderServiceDep,
    token_handler: Annotated[SupabaseTokenHandler, Depends(get_supabase_token_handler)],
) -> ListMyRidesQueryHandler:
    return ListMyRidesQueryHandler(ride_service, rider_service, token_handler)

GetRideHandlerDep = Annotated[GetRideQueryHandler, Depends(get_ride_query_handler)]
ListMyRidesHandlerDep = Annotated[ListMyRidesQueryHandler, Depends(get_list_my_rides_handler)]


# ── Ride commands ─────────────────────────────────────────────────────────────

def get_request_ride_handler(
    ride_service: RideServiceDep,
    rider_service: RiderServiceDep,
    token_handler: Annotated[SupabaseTokenHandler, Depends(get_supabase_token_handler)],
) -> RequestRideCommandHandler:
    return RequestRideCommandHandler(ride_service, rider_service, token_handler)

def get_assign_pod_handler(ride_service: RideServiceDep) -> AssignPodCommandHandler:
    return AssignPodCommandHandler(ride_service)

def get_board_ride_handler(ride_service: RideServiceDep) -> BoardRideCommandHandler:
    return BoardRideCommandHandler(ride_service)

def get_complete_ride_handler(ride_service: RideServiceDep) -> CompleteRideCommandHandler:
    return CompleteRideCommandHandler(ride_service)

def get_cancel_ride_handler(
    ride_service: RideServiceDep,
    rider_service: RiderServiceDep,
    token_handler: Annotated[SupabaseTokenHandler, Depends(get_supabase_token_handler)],
) -> CancelRideCommandHandler:
    return CancelRideCommandHandler(ride_service, rider_service, token_handler)

RequestRideHandlerDep = Annotated[RequestRideCommandHandler, Depends(get_request_ride_handler)]
AssignPodHandlerDep = Annotated[AssignPodCommandHandler, Depends(get_assign_pod_handler)]
BoardRideHandlerDep = Annotated[BoardRideCommandHandler, Depends(get_board_ride_handler)]
CompleteRideHandlerDep = Annotated[CompleteRideCommandHandler, Depends(get_complete_ride_handler)]
CancelRideHandlerDep = Annotated[CancelRideCommandHandler, Depends(get_cancel_ride_handler)]

