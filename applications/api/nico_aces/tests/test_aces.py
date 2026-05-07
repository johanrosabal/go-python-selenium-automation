import pytest
import allure
from core.api.common.base_api_test import BaseAPITest

@allure.epic("API")
@allure.feature("ACES Policy Search")
class TestNicoAces(BaseAPITest):
    """
    Test suite for the Nico ACES API.
    """
    app_name = "nico_aces"

    @pytest.mark.parametrize("test_data", BaseAPITest.load_test_data("nico_aces", "ACES-001"))
    def test_complete_aces_flow(self, test_data):
        """
        Verify the complete flow: Search -> Get Policies.
        """
        self.apply_test_metadata(test_data)
        payload = test_data['data']['payload']

        with allure.step("Initiate ACES Policy Search"):
            search_response = self.app.aces.search_policies(payload)
            search_response.assert_status_code(201)
            search_id = search_response.body.strip()
            assert search_id, "Search ID should not be empty"

        with allure.step(f"Retrieve policies for Search ID: {search_id}"):
            results_response = self.app.aces.get_policies(search_id)
            results_response.assert_status_code(200)
            # Add more assertions based on expected response structure
