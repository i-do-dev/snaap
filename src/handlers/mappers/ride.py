from src.core.entities.ride_request import RideRequest
from src.handlers.contracts.ride import RideResult


class RideHandlerMapper:
    @staticmethod
    def entity_to_result(entity: RideRequest) -> RideResult:
        return RideResult(
            rde_id=entity.rde_id,
            rde_created_at=entity.rde_created_at,
            rde_boarding_time=entity.rde_boarding_time,
            rde_dropoff_time=entity.rde_dropoff_time,
            rde_amount_charged=entity.rde_amount_charged,
            rde_currency_charged=entity.rde_currency_charged,
            rdr_id=entity.rdr_id,
            ptl_id=entity.ptl_id,
            pod_id=entity.pod_id,
            rde_starting_dock=entity.rde_starting_dock,
            rde_ending_dock=entity.rde_ending_dock,
            state=entity.derived_state,
        )
