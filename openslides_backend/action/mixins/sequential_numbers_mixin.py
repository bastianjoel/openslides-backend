from typing import Any, Dict, Optional

from datastore.shared.util import DeletedModelsBehaviour

from ...models.models import Model
from ...services.datastore.interface import DatastoreService
from ...shared.filters import FilterOperator
from ..generics.create import CreateAction
from ..util.typing import ActionResultElement


class SequentialNumbersMixin(CreateAction):
    datastore: DatastoreService
    model: Model

    def get_sequential_number(self, meeting_id: int) -> int:
        """
        Creates a sequential number, unique per meeting and returns it
        """
        filter = FilterOperator("meeting_id", "=", meeting_id)

        number = self.datastore.max(
            collection=self.model.collection,
            filter=filter,
            field="sequential_number",
            get_deleted_models=DeletedModelsBehaviour.ALL_MODELS,
        )
        number = 1 if number is None else number + 1
        return number

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        instance = super().update_instance(instance)
        instance["sequential_number"] = self.get_sequential_number(
            instance["meeting_id"]
        )
        return instance

    def create_action_result_element(
        self, instance: Dict[str, Any]
    ) -> Optional[ActionResultElement]:
        result = super().create_action_result_element(instance)
        if result is None:
            result = {"id": instance["id"]}
        result["sequential_number"] = instance["sequential_number"]
        return result
