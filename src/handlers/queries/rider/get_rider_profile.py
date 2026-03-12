from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from src.adapters.security.supabase_token_handler import SupabaseTokenHandler
from src.core.services.rider import RiderService
from src.handlers.contracts.rider import RiderProfileResult
from src.handlers.errors import AuthenticationError
from src.handlers.mappers.rider import RiderHandlerMapper


class GetRiderProfileQueryHandler:
    def __init__(self, rider_service: RiderService, token_handler: SupabaseTokenHandler) -> None:
        self.rider_service = rider_service
        self.token_handler = token_handler

    async def get_profile(self, token: str) -> RiderProfileResult:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc
        rider = await self.rider_service.get_or_provision(payload.email)
        return RiderHandlerMapper.entity_to_profile_result(rider)
