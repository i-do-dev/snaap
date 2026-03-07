from src.core.entities.pod import Pod
from src.handlers.contracts.pod import PodResult


class PodHandlerMapper:
    @staticmethod
    def entity_to_result(entity: Pod) -> PodResult:
        return PodResult(
            pod_id=entity.pod_id,
            pod_created_at=entity.pod_created_at,
            pod_name=entity.pod_name,
            pod_description=entity.pod_description,
            pod_configuration=entity.pod_configuration,
            pod_current_status=entity.pod_current_status,
            pod_current_location=entity.pod_current_location,
            rbn_id=entity.rbn_id,
        )
