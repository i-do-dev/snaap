from datetime import datetime, timezone
from decimal import Decimal
from typing import Sequence
from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.ride_request import RideRequest
from src.handlers.errors import ConflictError, NotFoundError, ValidationError


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RideService:
    """Domain service encapsulating ride lifecycle business rules."""

    def __init__(self, db: UnitOfWork) -> None:
        self.db = db

    async def request_ride(
        self, rdr_id: UUID, ptl_id: UUID, starting_dock: UUID, ending_dock: UUID
    ) -> RideRequest:
        if await self.db.portal.get(ptl_id) is None:
            raise NotFoundError(f"Portal {ptl_id} not found")
        if await self.db.dock.get(starting_dock) is None:
            raise NotFoundError(f"Starting dock {starting_dock} not found")
        if await self.db.dock.get(ending_dock) is None:
            raise NotFoundError(f"Ending dock {ending_dock} not found")
        entity = RideRequest(
            rdr_id=rdr_id,
            ptl_id=ptl_id,
            rde_starting_dock=starting_dock,
            rde_ending_dock=ending_dock,
        )
        return await self.db.ride_request.add(entity)

    async def get_ride(self, rde_id: UUID, rdr_id: UUID) -> RideRequest:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rdr_id != rdr_id:
            raise ValidationError("Access denied to this ride")
        return entity

    async def list_by_rider(
        self, rdr_id: UUID, offset: int = 0, limit: int = 50
    ) -> Sequence[RideRequest]:
        return await self.db.ride_request.list_by_rider(rdr_id, offset=offset, limit=limit)

    async def assign_pod(self, rde_id: UUID, pod_id: UUID) -> RideRequest:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.pod_id is not None and entity.rde_dropoff_time is None:
            raise ConflictError("Pod already assigned to this ride")
        pod = await self.db.pod.get(pod_id)
        if pod is None:
            raise NotFoundError(f"Pod {pod_id} not found")
        if pod.pod_current_status != "idle":
            raise ConflictError(f"Pod {pod_id} is not idle (status: {pod.pod_current_status})")
        updated = await self.db.ride_request.update_fields(rde_id, {"pod_id": pod_id})
        await self.db.pod.update_fields(pod_id, {"pod_current_status": "in_service"})
        return updated

    async def board(self, rde_id: UUID) -> RideRequest:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rde_boarding_time is not None:
            raise ConflictError("Ride boarding time already recorded")
        return await self.db.ride_request.update_fields(rde_id, {"rde_boarding_time": _utcnow()})

    async def complete(self, rde_id: UUID, amount: Decimal, currency: str) -> RideRequest:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rde_dropoff_time is not None:
            raise ConflictError("Ride already completed")
        updated = await self.db.ride_request.update_fields(rde_id, {
            "rde_dropoff_time": _utcnow(),
            "rde_amount_charged": amount,
            "rde_currency_charged": currency,
        })
        if entity.pod_id:
            await self.db.pod.update_fields(entity.pod_id, {"pod_current_status": "idle"})
        return updated

    async def cancel(self, rde_id: UUID, rdr_id: UUID) -> None:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rdr_id != rdr_id:
            raise ValidationError("Access denied to this ride")
        if entity.rde_boarding_time is not None:
            raise ConflictError("Cannot cancel a ride that has already started boarding")
        if entity.pod_id:
            await self.db.pod.update_fields(entity.pod_id, {"pod_current_status": "idle"})
        await self.db.ride_request.delete(entity)
