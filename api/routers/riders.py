from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from api.contracts.rider import RiderUpdateRequest, RiderProfileResponse
from api.dependencies.amms import (
    RiderBearerToken,
    GetRiderProfileHandlerDep,
    UpdateRiderProfileHandlerDep,
    ListMyRidesHandlerDep,
)
from api.contracts.ride import RideResponse
from src.handlers.contracts.rider import RiderUpdateCommand
from src.handlers.errors import AuthenticationError, NotFoundError

router = APIRouter(prefix="/riders", tags=["riders"])


@router.get("/me", response_model=RiderProfileResponse)
async def me(bearer_token: RiderBearerToken, handler: GetRiderProfileHandlerDep):
    """
    Returns the rider profile for the authenticated Supabase user.
    Creates a minimal profile record on first call (lazy provisioning).
    """
    try:
        result = await handler.get_profile(bearer_token)
        return RiderProfileResponse(**result.__dict__)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.patch("/me", response_model=RiderProfileResponse)
async def update_me(
    bearer_token: RiderBearerToken,
    request: RiderUpdateRequest,
    handler: UpdateRiderProfileHandlerDep,
):
    """Updates name, phone, and avatar for the authenticated rider."""
    command = RiderUpdateCommand(
        rdr_first_name=request.rdr_first_name,
        rdr_last_name=request.rdr_last_name,
        rdr_phone_number=request.rdr_phone_number,
        rdr_avatar=request.rdr_avatar,
    )
    try:
        result = await handler.update_profile(bearer_token, command)
        return RiderProfileResponse(**result.__dict__)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/me/rides", response_model=List[RideResponse])
async def my_rides(
    bearer_token: RiderBearerToken,
    handler: ListMyRidesHandlerDep,
    offset: int = 0,
    limit: int = 50,
):
    """Lists all ride requests for the authenticated rider."""
    try:
        results = await handler.list_my_rides(bearer_token, offset=offset, limit=limit)
        return [RideResponse(**r.__dict__) for r in results]
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
