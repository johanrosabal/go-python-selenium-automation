import pytest
from typing import TYPE_CHECKING
from core.api.common.base_api_test import BaseAPITest
from core.utils.decorators import test_case

if TYPE_CHECKING:
    from applications.api.nico_search.client import NicoSearchClient



class TestNicoSearch(BaseAPITest):
    """
    Test suite for nico_search - Policy Search API.
    self.app is automatically instantiated by BaseAPITest as NicoSearchClient.
    All test data is loaded from data/qa/SEARCH-XXX.json — zero hardcode.
    JSON structure: tests.data.payload (follows README standard).
    Allure metadata (title, description, severity, tags, feature, story)
    is injected automatically from the JSON — no need to repeat in the decorator.
    """
    app: 'NicoSearchClient'
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
        assert search_id is not None, f"Search initiation failed: {results_response.status_code}"
        results_response.assert_status_code(200)
        assert isinstance(results_response.body, list), "Expected results body to be a list"

        # Validate against expected results (if provided and not empty)
        expected_results = data["data"].get("expected_results", [])
        if expected_results:
            actual_results = results_response.body
            for expected in expected_results:
                match_found = False
                for actual in actual_results:
                    if all(actual.get(k) == v for k, v in expected.items()):
                        match_found = True
                        break
                assert match_found, f"Expected result not found in API response: {expected}"

        return search_id, results_response

    # =========================================================================
    # CATEGORY 1: Single-Field Searches
    # =========================================================================

    @test_case(id="SEARCH-001")
    def test_complete_search_flow(self):
        """Full end-to-end via orchestrator: search → GUID → get_results."""
        self._run_full_search_flow("SEARCH-001")

    @test_case(id="SEARCH-002")
    def test_search_by_first_last_name(self):
        """Validates searching by first and last name fields."""
        self._run_full_search_flow("SEARCH-002")

    @test_case(id="SEARCH-003")
    def test_search_by_policy_number(self):
        """Validates searching using an exact policy number."""
        self._run_full_search_flow("SEARCH-003")

    @test_case(id="SEARCH-004")
    def test_search_by_insured_name(self):
        """Validates searching using the full insured name."""
        self._run_full_search_flow("SEARCH-004")

    @test_case(id="SEARCH-005")
    def test_search_by_phone_number(self):
        """Validates searching by a registered phone number."""
        self._run_full_search_flow("SEARCH-005")

    @test_case(id="SEARCH-006")
    def test_search_by_vin(self):
        """Validates searching by a specific Vehicle Identification Number (VIN)."""
        self._run_full_search_flow("SEARCH-006")

    @test_case(id="SEARCH-007")
    def test_search_by_quote_number(self):
        """Validates searching using a quote number."""
        self._run_full_search_flow("SEARCH-007")

    @test_case(id="SEARCH-008")
    def test_search_by_agency_code(self):
        """Validates searching using an agency code."""
        self._run_full_search_flow("SEARCH-008")

    @test_case(id="SEARCH-009")
    def test_search_by_policy_state(self):
        """Validates searching for policies within a specific state."""
        self._run_full_search_flow("SEARCH-009")

    @test_case(id="SEARCH-010")
    def test_search_by_address(self):
        """Validates searching using a specific street address, city, state, and zip code."""
        self._run_full_search_flow("SEARCH-010")

    @test_case(id="SEARCH-011")
    def test_search_by_effective_date(self):
        """Validates searching policies by their effective date."""
        self._run_full_search_flow("SEARCH-011")

    @test_case(id="SEARCH-012")
    def test_search_by_email(self):
        """Validates searching using an insured email address."""
        self._run_full_search_flow("SEARCH-012")

    @test_case(id="SEARCH-013")
    def test_search_by_company_number(self):
        """Validates searching using only the company number."""
        self._run_full_search_flow("SEARCH-013")

    # =========================================================================
    # CATEGORY 2: Combined / Multi-Field Searches
    # =========================================================================

    @test_case(id="SEARCH-014")
    def test_search_combined_name_state(self):
        """Validates a combined search using both the insured's name and policy state."""
        self._run_full_search_flow("SEARCH-014")

    @test_case(id="SEARCH-015")
    def test_search_combined_agency_state(self):
        """Validates a combined search using both the agency code and policy state."""
        self._run_full_search_flow("SEARCH-015")
