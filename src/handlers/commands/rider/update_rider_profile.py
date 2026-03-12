from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from src.adapters.security.supabase_token_handler import SupabaseTokenHandler
from src.core.services.rider import RiderService
from src.handlers.contracts.rider import RiderProfileResult, RiderUpdateCommand
from src.handlers.errors import AuthenticationError
from src.handlers.mappers.rider import RiderHandlerMapper


class UpdateRiderProfileCommandHandler:
    def __init__(self, rider_service: RiderService, token_handler: SupabaseTokenHandler) -> None:
        self.rider_service = rider_service
        self.token_handler = token_handler

    async def update_profile(self, token: str, command: RiderUpdateCommand) -> RiderProfileResult:
        try:
            payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc
        rider = await self.rider_service.get_or_provision(payload.email)
        values = {k: v for k, v in {
            "rdr_first_name": command.rdr_first_name,
            "rdr_last_name": command.rdr_last_name,
            "rdr_phone_number": command.rdr_phone_number,
            "rdr_avatar": command.rdr_avatar,
        }.items() if v is not None}
        if values:
            rider = await self.rider_service.update_profile(rider.rdr_id, values)
        return RiderHandlerMapper.entity_to_profile_result(rider)
