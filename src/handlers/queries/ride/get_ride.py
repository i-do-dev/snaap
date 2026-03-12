from uuid import UUID
from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from src.adapters.security.supabase_token_handler import SupabaseTokenHandler
from src.core.services.ride import RideService
from src.core.services.rider import RiderService
from src.handlers.contracts.ride import RideResult
from src.handlers.errors import AuthenticationError
from src.handlers.mappers.ride import RideHandlerMapper


class GetRideQueryHandler:
    def __init__(
        self,
        ride_service: RideService,
        rider_service: RiderService,
        token_handler: SupabaseTokenHandler,
    ) -> None:
        self.ride_service = ride_service
        self.rider_service = rider_service
        self.token_handler = token_handler

    async def get_ride(self, token: str, rde_id: UUID) -> RideResult:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc
        rider = await self.rider_service.get_or_provision(payload.email)
        entity = await self.ride_service.get_ride(rde_id, rider.rdr_id)
        return RideHandlerMapper.entity_to_result(entity)
