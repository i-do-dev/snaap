from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.contracts.rider import RiderRegisterRequest, RiderUpdateRequest, RiderProfileResponse
from api.contracts.token import Token
from api.dependencies.amms import (
    RiderBearerToken, RiderSignupHandlerDep, RiderSigninHandlerDep,
    RiderProfileHandlerDep, RiderUpdateHandlerDep, RideHandler,
)
from api.contracts.ride import RideResponse
from src.handlers.contracts.rider import RiderSignUpCommand, RiderUpdateCommand
from src.handlers.errors import AuthenticationError, ConflictError, ValidationError, NotFoundError

router = APIRouter(prefix="/riders", tags=["riders"])


@router.post("/register", response_model=RiderProfileResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RiderRegisterRequest, handler: RiderSignupHandlerDep):
    command = RiderSignUpCommand(
        rdr_email=request.rdr_email,
        rdr_password=request.rdr_password,
        rdr_confirm_password=request.rdr_confirm_password,
        rdr_first_name=request.rdr_first_name,
        rdr_last_name=request.rdr_last_name,
        rdr_phone_number=request.rdr_phone_number,
    )
    try:
        result = await handler.signup(command)
        return RiderProfileResponse(**result.__dict__)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    handler: RiderSigninHandlerDep,
):
    try:
        result = await handler.sign_in(form_data.username, form_data.password)
        return Token(access_token=result.access_token, token_type=result.token_type)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.get("/me", response_model=RiderProfileResponse)
async def me(bearer_token: RiderBearerToken, handler: RiderProfileHandlerDep):
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
    handler: RiderUpdateHandlerDep,
):
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


@router.get("/me/rides", response_model=List[RideResponse])
async def my_rides(
    bearer_token: RiderBearerToken,
    ride_handler: RideHandler,
    offset: int = 0,
    limit: int = 50,
):
    try:
        results = await ride_handler.list_my_rides(bearer_token, offset=offset, limit=limit)
        return [RideResponse(**r.__dict__) for r in results]
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
