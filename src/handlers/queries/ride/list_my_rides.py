from typing import Sequence
from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from src.adapters.security.supabase_token_handler import SupabaseTokenHandler
from src.core.services.ride import RideService
from src.core.services.rider import RiderService
from src.handlers.contracts.ride import RideResult
from src.handlers.errors import AuthenticationError
from src.handlers.mappers.ride import RideHandlerMapper


class ListMyRidesQueryHandler:
    def __init__(
        self,
        ride_service: RideService,
        rider_service: RiderService,
        token_handler: SupabaseTokenHandler,
    ) -> None:
        self.ride_service = ride_service
        self.rider_service = rider_service
        self.token_handler = token_handler

    async def list_my_rides(
        self, token: str, offset: int = 0, limit: int = 50
    ) -> Sequence[RideResult]:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc
        rider = await self.rider_service.get_or_provision(payload.email)
        entities = await self.ride_service.list_by_rider(rider.rdr_id, offset=offset, limit=limit)
        return [RideHandlerMapper.entity_to_result(e) for e in entities]
