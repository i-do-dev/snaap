from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from api.contracts.ribbonway import (
    RibbonwayCreateRequest, RibbonwayUpdateRequest, RibbonwayResponse,
    PortalCreateRequest, PortalResponse,
    DockCreateRequest, DockResponse,
)
from api.dependencies.amms import RibbonwayHandler
from src.handlers.contracts.ribbonway import (
    RibbonwayCreateCommand, RibbonwayUpdateCommand,
    PortalCreateCommand, DockCreateCommand,
)
from src.handlers.errors import ConflictError, NotFoundError

router = APIRouter(prefix="/ribbonways", tags=["ribbonways"])
portals_router = APIRouter(prefix="/portals", tags=["portals"])
docks_router = APIRouter(prefix="/docks", tags=["docks"])


# ── Ribbonway CRUD ────────────────────────────────────────────────────────────

@router.post("/", response_model=RibbonwayResponse, status_code=status.HTTP_201_CREATED)
async def create_ribbonway(request: RibbonwayCreateRequest, handler: RibbonwayHandler):
    command = RibbonwayCreateCommand(
        rbn_name=request.rbn_name,
        rbn_description=request.rbn_description,
        rbn_geofence_location=request.rbn_geofence_location,
    )
    result = await handler.create(command)
    return RibbonwayResponse(**result.__dict__)


@router.get("/", response_model=List[RibbonwayResponse])
async def list_ribbonways(handler: RibbonwayHandler, offset: int = 0, limit: int = 50):
    results = await handler.list_all(offset=offset, limit=limit)
    return [RibbonwayResponse(**r.__dict__) for r in results]


@router.get("/{rbn_id}", response_model=RibbonwayResponse)
async def get_ribbonway(rbn_id: UUID, handler: RibbonwayHandler):
    try:
        result = await handler.get(rbn_id)
        return RibbonwayResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{rbn_id}", response_model=RibbonwayResponse)
async def update_ribbonway(rbn_id: UUID, request: RibbonwayUpdateRequest, handler: RibbonwayHandler):
    command = RibbonwayUpdateCommand(
        rbn_name=request.rbn_name,
        rbn_description=request.rbn_description,
        rbn_geofence_location=request.rbn_geofence_location,
    )
    try:
        result = await handler.update(rbn_id, command)
        return RibbonwayResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{rbn_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ribbonway(rbn_id: UUID, handler: RibbonwayHandler):
    try:
        await handler.delete(rbn_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


# ── Portals (nested under ribbonways + standalone) ───────────────────────────

@router.post("/{rbn_id}/portals", response_model=PortalResponse, status_code=status.HTTP_201_CREATED)
async def create_portal(rbn_id: UUID, request: PortalCreateRequest, handler: RibbonwayHandler):
    command = PortalCreateCommand(
        rbn_id=rbn_id,
        ptl_name=request.ptl_name,
        ptl_description=request.ptl_description,
        ptl_geofence_location=request.ptl_geofence_location,
    )
    try:
        result = await handler.create_portal(command)
        return PortalResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{rbn_id}/portals", response_model=List[PortalResponse])
async def list_portals(rbn_id: UUID, handler: RibbonwayHandler):
    results = await handler.list_portals(rbn_id)
    return [PortalResponse(**r.__dict__) for r in results]


# ── Standalone portal endpoints ───────────────────────────────────────────────

@portals_router.get("/{ptl_id}", response_model=PortalResponse)
async def get_portal(ptl_id: UUID, handler: RibbonwayHandler):
    try:
        result = await handler.get_portal(ptl_id)
        return PortalResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@portals_router.post("/{ptl_id}/docks", response_model=DockResponse, status_code=status.HTTP_201_CREATED)
async def create_dock(ptl_id: UUID, request: DockCreateRequest, handler: RibbonwayHandler):
    command = DockCreateCommand(
        ptl_id=ptl_id,
        dck_name=request.dck_name,
        dck_description=request.dck_description,
        dck_geofence_location=request.dck_geofence_location,
    )
    try:
        result = await handler.create_dock(command)
        return DockResponse(**result.__dict__)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@portals_router.get("/{ptl_id}/docks", response_model=List[DockResponse])
async def list_docks(ptl_id: UUID, handler: RibbonwayHandler):
    results = await handler.list_docks(ptl_id)
    return [DockResponse(**r.__dict__) for r in results]
