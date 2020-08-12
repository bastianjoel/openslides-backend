from tests.system.base import BaseSystemTestCase
from tests.util import get_fqid


class MotionWorkflowSystemTest(BaseSystemTestCase):
    def test_create(self) -> None:
        response = self.client.post(
            "/",
            json=[
                {
                    "action": "motion_workflow.create",
                    "data": [{"name": "test_Xcdfgee"}],
                }
            ],
        )
        self.assertEqual(response.status_code, 200)
        self.assert_model_exists(get_fqid("motion_workflow/1"))
        model = self.datastore.get(get_fqid("motion_workflow/1"))
        assert model.get("name") == "test_Xcdfgee"

    def test_create_empty_data(self) -> None:
        response = self.client.post(
            "/", json=[{"action": "motion_workflow.create", "data": [{}]}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "data[0] must contain [\\'name\\'] properties", str(response.data),
        )

    def test_create_wrong_field(self) -> None:
        response = self.client.post(
            "/",
            json=[
                {
                    "action": "motion_workflow.create",
                    "data": [{"wrong_field": "text_AefohteiF8"}],
                }
            ],
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "data[0] must contain [\\'name\\'] properties", str(response.data),
        )
