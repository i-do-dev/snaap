from typing import Optional
from src.adapters.db.models import Rider as RiderModel
from src.core.entities.rider import Rider, SecureRider
from src.core.value_objects.password import HashedPassword


class RiderMapper:
    @staticmethod
    def model_to_entity(model: RiderModel) -> Optional[Rider]:
        if not model:
            return None
        return Rider(
            rdr_id=model.rdr_id,
            rdr_created_at=model.rdr_created_at,
            rdr_first_name=model.rdr_first_name,
            rdr_last_name=model.rdr_last_name,
            rdr_email=model.rdr_email,
            rdr_phone_number=model.rdr_phone_number,
            rdr_avatar=model.rdr_avatar,
        )

    @staticmethod
    def model_to_secure_entity(model: RiderModel) -> Optional[SecureRider]:
        if not model:
            return None
        return SecureRider(
            rdr_id=model.rdr_id,
            rdr_created_at=model.rdr_created_at,
            rdr_first_name=model.rdr_first_name,
            rdr_last_name=model.rdr_last_name,
            rdr_email=model.rdr_email,
            rdr_phone_number=model.rdr_phone_number,
            rdr_avatar=model.rdr_avatar,
            rdr_password=HashedPassword(model.rdr_password) if model.rdr_password else None,
        )

    @staticmethod
    def entity_to_model(entity: SecureRider) -> RiderModel:
        kwargs = {
            "rdr_first_name": entity.rdr_first_name,
            "rdr_last_name": entity.rdr_last_name,
            "rdr_email": entity.rdr_email,
            "rdr_phone_number": entity.rdr_phone_number,
            "rdr_avatar": entity.rdr_avatar,
            "rdr_password": entity.rdr_password.value if entity.rdr_password else None,
        }
        if entity.rdr_id is not None:
            kwargs["rdr_id"] = entity.rdr_id
        return RiderModel(**kwargs)
