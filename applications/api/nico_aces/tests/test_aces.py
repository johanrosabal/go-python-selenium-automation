import pytest
from typing import TYPE_CHECKING
from core.api.common.base_api_test import BaseAPITest
from core.utils.decorators import test_case

if TYPE_CHECKING:
    from applications.api.nico_aces.client import NicoAcesClient


class TestNicoAces(BaseAPITest):
    """
    Test suite for the Nico ACES API.
    self.app is automatically instantiated by BaseAPITest as NicoAcesClient.
    All test data is loaded from data/qa/ACES-XXX.json — zero hardcode.
    JSON structure: tests.data.payload (follows README standard).
    Allure metadata (title, description, severity, tags, feature, story)
    is injected automatically from the JSON — no need to repeat in the decorator.
    """

    app: "NicoAcesClient"
    app_name = "nico_aces"

    def _run_full_aces_flow(self, test_id=None):
        """Helper: loads JSON payload, runs the full search-and-get-policies flow, and asserts response correctness."""
        data = self.get_test_data(test_id)
        payload = data["data"]["payload"]
        search_id, results_response = self.app.search_and_get_policies(payload)

        # Skip if auth/IP block is detected during the flow
        if results_response.status_code in [401, 403]:
            pytest.skip("Unauthorized or IP Forbidden.")

        # Ensure search succeeded and we received results
        assert (
            search_id is not None
        ), f"Search initiation failed: {results_response.status_code}"
        results_response.assert_status_code(200)
        assert isinstance(
            results_response.body, list
        ), "Expected results body to be a list"

        # Validate against expected results (if provided and not empty)
        expected_results = data["data"].get("expected_results", [])
        if expected_results:
            actual_results = results_response.body
            for expected in expected_results:
                match_found = False
                closest_match = None
                max_matched_keys = -1

                for actual in actual_results:
                    matched_keys = sum(
                        1 for k, v in expected.items() if actual.get(k) == v
                    )
                    if matched_keys == len(expected):
                        match_found = True
                        break

                    if matched_keys > max_matched_keys:
                        max_matched_keys = matched_keys
                        closest_match = actual

                if not match_found:
                    error_msg = f"Expected result not found in API response.\n\nEXPECTED:\n{expected}\n"
                    if closest_match and max_matched_keys > 0:
                        mismatches = {
                            k: {"expected": v, "actual": closest_match.get(k)}
                            for k, v in expected.items()
                            if closest_match.get(k) != v
                        }
                        error_msg += f"\nCLOSEST ACTUAL MATCH FOUND:\n{closest_match}\n\nMISMATCHED FIELDS:\n{mismatches}"
                    else:
                        error_msg += f"\nACTUAL RESULTS RETURNED ({len(actual_results)} items):\n{actual_results}"

                    pytest.fail(error_msg)

        return search_id, results_response

    @test_case(id="ACES-001")
    def test_complete_aces_search_flow_default(self):
        self._run_full_aces_flow("ACES-001")

    @test_case(id="ACES-002")
    def test_search_by_insured_name_and_company_2(self):
        self._run_full_aces_flow("ACES-002")

    @test_case(id="ACES-003")
    def test_search_by_insured_name_and_company_1(self):
        self._run_full_aces_flow("ACES-003")

    @test_case(id="ACES-004")
    def test_search_by_first_name_and_last_name_company_2(self):
        self._run_full_aces_flow("ACES-004")

    @test_case(id="ACES-005")
    def test_search_by_first_name_and_last_name_company_2_alt(self):
        self._run_full_aces_flow("ACES-005")

    @test_case(id="ACES-006")
    def test_search_by_policy_number_company_1(self):
        self._run_full_aces_flow("ACES-006")

    @test_case(id="ACES-007")
    def test_search_by_policy_number_company_2(self):
        self._run_full_aces_flow("ACES-007")

    @test_case(id="ACES-008")
    def test_search_by_quote_number_company_1(self):
        self._run_full_aces_flow("ACES-008")

    @test_case(id="ACES-009")
    def test_search_by_quote_number_company_2(self):
        self._run_full_aces_flow("ACES-009")

    @test_case(id="ACES-010")
    def test_search_by_phone_number_company_1(self):
        """Search by Phone Number Company 1"""
        self._run_full_aces_flow("ACES-010")

    @test_case(id="ACES-011")
    def test_search_by_phone_number_company_2(self):
        self._run_full_aces_flow("ACES-011")

    @test_case(id="ACES-012")
    def test_search_by_vin_company_1(self):
        self._run_full_aces_flow("ACES-012")

    @test_case(id="ACES-013")
    def test_search_by_vin_company_2(self):
        self._run_full_aces_flow("ACES-013")

    @test_case(id="ACES-014")
    def test_search_by_single_agent_code_and_policy_number_company_1(self):
        self._run_full_aces_flow("ACES-014")

    @test_case(id="ACES-015")
    def test_search_by_single_agent_code_and_policy_number_company_2(self):
        self._run_full_aces_flow("ACES-015")

    @test_case(id="ACES-016")
    def test_search_by_quote_number_without_policy_number_company_1(self):
        self._run_full_aces_flow("ACES-016")
