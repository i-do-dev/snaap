from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from api.contracts.ride import RideRequestCreate, RideAssignRequest, RideCompleteRequest, RideResponse
from api.dependencies.amms import (
    RiderBearerToken,
    RequestRideHandlerDep,
    GetRideHandlerDep,
    AssignPodHandlerDep,
    BoardRideHandlerDep,
    CompleteRideHandlerDep,
    CancelRideHandlerDep,
)
from src.handlers.contracts.ride import RideRequestCommand, RideAssignCommand, RideCompleteCommand
from src.handlers.errors import AuthenticationError, ConflictError, NotFoundError, ValidationError

router = APIRouter(prefix="/rides", tags=["rides"])


@router.post("/", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
async def request_ride(
    bearer_token: RiderBearerToken,
    request: RideRequestCreate,
    handler: RequestRideHandlerDep,
):
    command = RideRequestCommand(
        ptl_id=request.ptl_id,
        rde_starting_dock=request.rde_starting_dock,
        rde_ending_dock=request.rde_ending_dock,
    )
    try:
        result = await handler.request_ride(bearer_token, command)
        return RideResponse(**result.__dict__)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc),
                            headers={"WWW-Authenticate": "Bearer"}) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{rde_id}", response_model=RideResponse)
async def get_ride(rde_id: UUID, bearer_token: RiderBearerToken, handler: GetRideHandlerDep):
    try:
        result = await handler.get_ride(bearer_token, rde_id)
        return RideResponse(**result.__dict__)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc),
                            headers={"WWW-Authenticate": "Bearer"}) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{rde_id}/assign", response_model=RideResponse)
async def assign_pod(rde_id: UUID, request: RideAssignRequest, handler: AssignPodHandlerDep):
    command = RideAssignCommand(pod_id=request.pod_id)
    try:
        result = await handler.assign_pod(rde_id, command)
        return RideResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{rde_id}/board", response_model=RideResponse)
async def board_ride(rde_id: UUID, handler: BoardRideHandlerDep):
    try:
        result = await handler.board_ride(rde_id)
        return RideResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{rde_id}/complete", response_model=RideResponse)
async def complete_ride(rde_id: UUID, request: RideCompleteRequest, handler: CompleteRideHandlerDep):
    command = RideCompleteCommand(
        rde_amount_charged=request.rde_amount_charged,
        rde_currency_charged=request.rde_currency_charged,
    )
    try:
        result = await handler.complete_ride(rde_id, command)
        return RideResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.delete("/{rde_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_ride(rde_id: UUID, bearer_token: RiderBearerToken, handler: CancelRideHandlerDep):
    try:
        await handler.cancel_ride(bearer_token, rde_id)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc),
                            headers={"WWW-Authenticate": "Bearer"}) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
