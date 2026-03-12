from uuid import UUID
from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from src.adapters.security.supabase_token_handler import SupabaseTokenHandler
from src.core.services.ride import RideService
from src.core.services.rider import RiderService
from src.handlers.errors import AuthenticationError


class CancelRideCommandHandler:
    """Rider-facing: cancels a pending ride (not yet boarding)."""

    def __init__(
        self,
        ride_service: RideService,
        rider_service: RiderService,
        token_handler: SupabaseTokenHandler,
    ) -> None:
        self.ride_service = ride_service
        self.rider_service = rider_service
        self.token_handler = token_handler

    async def cancel_ride(self, token: str, rde_id: UUID) -> None:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc
        rider = await self.rider_service.get_or_provision(payload.email)
        await self.ride_service.cancel(rde_id, rider.rdr_id)
