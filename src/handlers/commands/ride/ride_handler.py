from datetime import datetime, timezone
from typing import Sequence
from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.ride_request import RideRequest, RideState
from src.core.services.token_handler import ITokenHandler
from src.handlers.contracts.ride import (
    RideRequestCommand, RideAssignCommand, RideCompleteCommand, RideResult,
)
from src.handlers.errors import AuthenticationError, ConflictError, NotFoundError
from src.handlers.mappers.ride import RideHandlerMapper

_COULD_NOT_VALIDATE = "Could not validate credentials"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RideRequestCommandHandler:
    def __init__(self, db: UnitOfWork, token_handler: ITokenHandler) -> None:
        self.db = db
        self.token_handler = token_handler

    async def _get_rider_id(self, token: str) -> UUID:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(_COULD_NOT_VALIDATE) from exc
        rider = await self.db.rider.get_by_email(payload.sub)
        if rider is None:
            raise AuthenticationError(_COULD_NOT_VALIDATE)
        return rider.rdr_id

    async def request_ride(self, token: str, command: RideRequestCommand) -> RideResult:
        rdr_id = await self._get_rider_id(token)
        # Validate portal exists
        portal = await self.db.portal.get(command.ptl_id)
        if portal is None:
            raise NotFoundError(f"Portal {command.ptl_id} not found")
        # Validate docks exist (application-level; no DB FK)
        starting_dock = await self.db.dock.get(command.rde_starting_dock)
        if starting_dock is None:
            raise NotFoundError(f"Starting dock {command.rde_starting_dock} not found")
        ending_dock = await self.db.dock.get(command.rde_ending_dock)
        if ending_dock is None:
            raise NotFoundError(f"Ending dock {command.rde_ending_dock} not found")

        entity = RideRequest(
            rdr_id=rdr_id,
            ptl_id=command.ptl_id,
            rde_starting_dock=command.rde_starting_dock,
            rde_ending_dock=command.rde_ending_dock,
        )
        created = await self.db.ride_request.add(entity)
        return RideHandlerMapper.entity_to_result(created)

    async def get_ride(self, token: str, rde_id: UUID) -> RideResult:
        rdr_id = await self._get_rider_id(token)
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rdr_id != rdr_id:
            from src.handlers.errors import ValidationError
            raise ValidationError("Access denied to this ride")
        return RideHandlerMapper.entity_to_result(entity)

    async def list_my_rides(self, token: str, offset: int = 0, limit: int = 50) -> Sequence[RideResult]:
        rdr_id = await self._get_rider_id(token)
        entities = await self.db.ride_request.list_by_rider(rdr_id, offset=offset, limit=limit)
        return [RideHandlerMapper.entity_to_result(e) for e in entities]

    async def assign_pod(self, rde_id: UUID, command: RideAssignCommand) -> RideResult:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.pod_id is not None and entity.rde_dropoff_time is None:
            raise ConflictError("Pod already assigned to this ride")
        pod = await self.db.pod.get(command.pod_id)
        if pod is None:
            raise NotFoundError(f"Pod {command.pod_id} not found")
        if pod.pod_current_status != "idle":
            raise ConflictError(f"Pod {command.pod_id} is not idle (status: {pod.pod_current_status})")
        # Assign pod to ride
        updated = await self.db.ride_request.update_fields(rde_id, {"pod_id": command.pod_id})
        # Update pod status to in_service
        await self.db.pod.update_fields(command.pod_id, {"pod_current_status": "in_service"})
        return RideHandlerMapper.entity_to_result(updated)

    async def board_ride(self, rde_id: UUID) -> RideResult:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rde_boarding_time is not None:
            raise ConflictError("Ride boarding time already recorded")
        updated = await self.db.ride_request.update_fields(rde_id, {"rde_boarding_time": _utcnow()})
        return RideHandlerMapper.entity_to_result(updated)

    async def complete_ride(self, rde_id: UUID, command: RideCompleteCommand) -> RideResult:
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rde_dropoff_time is not None:
            raise ConflictError("Ride already completed")
        updated = await self.db.ride_request.update_fields(rde_id, {
            "rde_dropoff_time": _utcnow(),
            "rde_amount_charged": command.rde_amount_charged,
            "rde_currency_charged": command.rde_currency_charged,
        })
        # Return pod to idle
        if entity.pod_id:
            await self.db.pod.update_fields(entity.pod_id, {"pod_current_status": "idle"})
        return RideHandlerMapper.entity_to_result(updated)

    async def cancel_ride(self, token: str, rde_id: UUID) -> None:
        rdr_id = await self._get_rider_id(token)
        entity = await self.db.ride_request.get(rde_id)
        if entity is None:
            raise NotFoundError(f"Ride {rde_id} not found")
        if entity.rdr_id != rdr_id:
            from src.handlers.errors import ValidationError
            raise ValidationError("Access denied to this ride")
        if entity.rde_boarding_time is not None:
            raise ConflictError("Cannot cancel a ride that has already started boarding")
        # Return pod to idle if assigned
        if entity.pod_id:
            await self.db.pod.update_fields(entity.pod_id, {"pod_current_status": "idle"})
        await self.db.ride_request.delete(entity)
