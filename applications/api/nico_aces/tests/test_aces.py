import pytest
import allure
from core.api.common.base_api_test import BaseAPITest
from core.utils.decorators import test_case

@allure.epic("API")
@allure.feature("ACES Policy Search")
class TestNicoAces(BaseAPITest):
    """
    Test suite for the Nico ACES API.
    """
    app_name = "nico_aces"

    @test_case(id="ACES-001")
    def test_complete_aces_flow(self):
        """
        Verify the complete flow: Search -> Get Policies.
        """
        # Data is automatically loaded into self._current_test_data by the @test_case decorator
        payload = self._current_test_data.get('payload')
        assert payload, "Payload not found in test data"

        with allure.step("Initiate ACES Policy Search"):
            search_response = self.app.aces.search_policies(payload)
            
            # Skip if auth/IP block is detected
            if search_response.status_code in [401, 403]:
                pytest.skip(f"Request blocked (Status: {search_response.status_code})")
                
            search_response.assert_status_code(201)
            search_id = search_response.body.strip()
            assert search_id, "Search ID should not be empty"

        with allure.step(f"Retrieve policies for Search ID: {search_id}"):
            results_response = self.app.aces.get_policies(search_id)
            results_response.assert_status_code(200)
            # Add more assertions based on expected response structure
