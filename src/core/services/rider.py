from typing import Optional
from uuid import UUID
from src.adapters.db.uow import UnitOfWork
from src.core.entities.rider import Rider
from src.handlers.errors import NotFoundError


class RiderService:
    """Domain service for rider profile lifecycle operations."""

    def __init__(self, db: UnitOfWork) -> None:
        self.db = db

    async def get_or_provision(self, email: str) -> Rider:
        """
        Return the snaap_riders row for the given email.
        Creates a minimal profile record on first call — lazy Supabase sync.
        """
        rider = await self.db.rider.get_by_email(email)
        if rider is None:
            rider = await self.db.rider.add(Rider(rdr_email=email))
        return rider

    async def get_by_email(self, email: str) -> Optional[Rider]:
        return await self.db.rider.get_by_email(email)

    async def update_profile(self, rdr_id: UUID, values: dict) -> Rider:
        updated = await self.db.rider.update_fields(rdr_id, values)
        if updated is None:
            raise NotFoundError(f"Rider {rdr_id} not found")
        return updated
