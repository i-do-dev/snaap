from typing import Annotated, List
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.contracts.rider import RiderUpdateRequest, RiderProfileResponse
from api.contracts.token import Token
from api.dependencies.amms import (
    RiderBearerToken,
    GetRiderProfileHandlerDep,
    UpdateRiderProfileHandlerDep,
    ListMyRidesHandlerDep,
)
from api.contracts.ride import RideResponse
from src.handlers.contracts.rider import RiderUpdateCommand
from src.handlers.errors import AuthenticationError, NotFoundError
from settings import Settings

router = APIRouter(prefix="/riders", tags=["riders"])


@router.post("/token", response_model=Token, include_in_schema=False)
async def rider_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Proxies rider credentials to Supabase and returns the access token.
    This endpoint exists solely to make Swagger UI's Authorize button functional
    for the RiderOAuth2 scheme.  In production, mobile clients exchange credentials
    directly with Supabase and pass the resulting JWT to rider/ride endpoints.
    """
    settings = Settings()
    url = f"{settings.supabase_url.rstrip('/')}/auth/v1/token?grant_type=password"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers={"apikey": settings.supabase_anon_key, "Content-Type": "application/json"},
            json={"email": form_data.username, "password": form_data.password},
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid rider credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=resp.json()["access_token"], token_type="bearer")


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
