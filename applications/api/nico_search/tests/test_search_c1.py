import pytest
from typing import TYPE_CHECKING
from core.api.common.base_api_test import BaseAPITest
from core.utils.decorators import test_case

if TYPE_CHECKING:
    from applications.api.nico_search.client import NicoSearchClient


class TestNicoSearchCompany1(BaseAPITest):
    """
    Test suite for nico_search - Policy Search API.
    self.app is automatically instantiated by BaseAPITest as NicoSearchClient.
    All test data is loaded from data/qa/SEARCH-XXX.json — zero hardcode.
    JSON structure: tests.data.payload (follows README standard).
    Allure metadata (title, description, severity, tags, feature, story)
    is injected automatically from the JSON — no need to repeat in the decorator.
    """

    app: "NicoSearchClient"
    app_name = "nico_search"

    def _run_full_search_flow(self, test_id=None):
        """Helper: loads JSON payload, runs the full search-and-get-results flow, and asserts response correctness."""
        data = self.get_test_data(test_id)
        payload = data["data"]["payload"]
        search_id, results_response = self.app.search_and_get_results(payload)

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

    # =========================================================================
    # CATEGORY 1: Single-Field Searches
    # =========================================================================

    @test_case(id="SEARCH-001-C1")
    def test_complete_search_flow(self):
        self._run_full_search_flow("SEARCH-001-C1")

    @test_case(id="SEARCH-002-C1")
    def test_search_by_first_last_name(self):
        self._run_full_search_flow("SEARCH-002-C1")

    @test_case(id="SEARCH-003-C1")
    def test_search_by_policy_number(self):
        self._run_full_search_flow("SEARCH-003-C1")

    @test_case(id="SEARCH-004-C1")
    def test_search_by_insured_name(self):
        self._run_full_search_flow("SEARCH-004-C1")

    @test_case(id="SEARCH-005-C1")
    def test_search_by_phone_number(self):
        self._run_full_search_flow("SEARCH-005-C1")

    @test_case(id="SEARCH-006-C1")
    def test_search_by_vin(self):
        self._run_full_search_flow("SEARCH-006-C1")

    @test_case(id="SEARCH-007-C1")
    def test_search_by_quote_number(self):
        self._run_full_search_flow("SEARCH-007-C1")

    @test_case(id="SEARCH-008-C1")
    def test_search_by_agency_code(self):
        self._run_full_search_flow("SEARCH-008-C1")

    @test_case(id="SEARCH-009-C1")
    def test_search_by_policy_state(self):
        self._run_full_search_flow("SEARCH-009-C1")

    @test_case(id="SEARCH-010-C1")
    def test_search_by_address(self):
        self._run_full_search_flow("SEARCH-010-C1")

    @test_case(id="SEARCH-011-C1")
    def test_search_by_effective_date(self):
        self._run_full_search_flow("SEARCH-011-C1")
