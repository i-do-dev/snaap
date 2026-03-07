from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status
from api.contracts.pod import PodCreateRequest, PodUpdateRequest, PodResponse
from api.dependencies.amms import PodHandler
from src.handlers.contracts.pod import PodCreateCommand, PodUpdateCommand
from src.handlers.errors import ConflictError, NotFoundError, ValidationError

router = APIRouter(prefix="/pods", tags=["pods"])


@router.post("/", response_model=PodResponse, status_code=status.HTTP_201_CREATED)
async def create_pod(request: PodCreateRequest, handler: PodHandler):
    command = PodCreateCommand(
        pod_current_location=request.pod_current_location,
        pod_name=request.pod_name,
        pod_description=request.pod_description,
        pod_configuration=request.pod_configuration,
        rbn_id=request.rbn_id,
    )
    result = await handler.create(command)
    return PodResponse(**result.__dict__)


@router.get("/", response_model=List[PodResponse])
async def list_pods(
    handler: PodHandler,
    offset: int = 0,
    limit: int = 50,
    status: Optional[str] = Query(default=None),
    rbn_id: Optional[UUID] = Query(default=None),
):
    results = await handler.list_all(offset=offset, limit=limit, status=status, rbn_id=rbn_id)
    return [PodResponse(**r.__dict__) for r in results]


@router.get("/{pod_id}", response_model=PodResponse)
async def get_pod(pod_id: UUID, handler: PodHandler):
    try:
        result = await handler.get(pod_id)
        return PodResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{pod_id}", response_model=PodResponse)
async def update_pod(pod_id: UUID, request: PodUpdateRequest, handler: PodHandler):
    command = PodUpdateCommand(
        pod_current_status=request.pod_current_status,
        pod_current_location=request.pod_current_location,
        rbn_id=request.rbn_id,
        pod_name=request.pod_name,
        pod_description=request.pod_description,
        pod_configuration=request.pod_configuration,
    )
    try:
        result = await handler.update(pod_id, command)
        return PodResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.delete("/{pod_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pod(pod_id: UUID, handler: PodHandler):
    try:
        await handler.delete(pod_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
