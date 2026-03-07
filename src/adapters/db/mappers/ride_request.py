from src.adapters.db.models import RideRequest as RideRequestModel
from src.core.entities.ride_request import RideRequest


class RideRequestMapper:
    @staticmethod
    def model_to_entity(model: RideRequestModel) -> RideRequest:
        return RideRequest(
            rde_id=model.rde_id,
            rde_created_at=model.rde_created_at,
            rde_boarding_time=model.rde_boarding_time,
            rde_dropoff_time=model.rde_dropoff_time,
            rde_amount_charged=model.rde_amount_charged,
            rde_currency_charged=model.rde_currency_charged,
            rdr_id=model.rdr_id,
            ptl_id=model.ptl_id,
            pod_id=model.pod_id,
            rde_starting_dock=model.rde_starting_dock,
            rde_ending_dock=model.rde_ending_dock,
        )

    @staticmethod
    def entity_to_model(entity: RideRequest) -> RideRequestModel:
        kwargs = {
            "rde_boarding_time": entity.rde_boarding_time,
            "rde_dropoff_time": entity.rde_dropoff_time,
            "rde_amount_charged": entity.rde_amount_charged,
            "rde_currency_charged": entity.rde_currency_charged,
            "rdr_id": entity.rdr_id,
            "ptl_id": entity.ptl_id,
            "pod_id": entity.pod_id,
            "rde_starting_dock": entity.rde_starting_dock,
            "rde_ending_dock": entity.rde_ending_dock,
        }
        if entity.rde_id is not None:
            kwargs["rde_id"] = entity.rde_id
        return RideRequestModel(**kwargs)
