from src.adapters.db.models import Pod as PodModel
from src.core.entities.pod import Pod


class PodMapper:
    @staticmethod
    def model_to_entity(model: PodModel) -> Pod:
        return Pod(
            pod_id=model.pod_id,
            pod_created_at=model.pod_created_at,
            pod_name=model.pod_name,
            pod_description=model.pod_description,
            pod_configuration=model.pod_configuration,
            pod_current_status=model.pod_current_status,
            pod_current_location=model.pod_current_location,
            rbn_id=model.rbn_id,
        )

    @staticmethod
    def entity_to_model(entity: Pod) -> PodModel:
        kwargs = {
            "pod_name": entity.pod_name,
            "pod_description": entity.pod_description,
            "pod_configuration": entity.pod_configuration,
            "pod_current_status": entity.pod_current_status,
            "pod_current_location": entity.pod_current_location,
            "rbn_id": entity.rbn_id,
        }
        if entity.pod_id is not None:
            kwargs["pod_id"] = entity.pod_id
        return PodModel(**kwargs)
