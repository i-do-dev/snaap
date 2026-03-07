from src.core.entities.rider import Rider
from src.handlers.contracts.rider import RiderProfileResult


class RiderHandlerMapper:
    @staticmethod
    def entity_to_profile_result(entity: Rider) -> RiderProfileResult:
        return RiderProfileResult(
            rdr_id=entity.rdr_id,
            rdr_created_at=entity.rdr_created_at,
            rdr_email=entity.rdr_email,
            rdr_first_name=entity.rdr_first_name,
            rdr_last_name=entity.rdr_last_name,
            rdr_phone_number=entity.rdr_phone_number,
            rdr_avatar=entity.rdr_avatar,
        )
