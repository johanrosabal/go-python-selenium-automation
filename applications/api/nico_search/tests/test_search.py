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
        self._run_full_search_flow("SEARCH-002")

    @test_case(id="SEARCH-003")
    def test_search_by_policy_number(self):
        self._run_full_search_flow("SEARCH-003")

    @test_case(id="SEARCH-004")
    def test_search_by_insured_name(self):
        self._run_full_search_flow("SEARCH-004")

    @test_case(id="SEARCH-005")
    def test_search_by_phone_number(self):
        self._run_full_search_flow("SEARCH-005")

    @test_case(id="SEARCH-006")
    def test_search_by_vin(self):
        self._run_full_search_flow("SEARCH-006")

    @test_case(id="SEARCH-007")
    def test_search_by_quote_number(self):
        self._run_full_search_flow("SEARCH-007")

    @test_case(id="SEARCH-008")
    def test_search_by_agency_code(self):
        self._run_full_search_flow("SEARCH-008")

    @test_case(id="SEARCH-009")
    def test_search_by_policy_state(self):
        self._run_full_search_flow("SEARCH-009")

    @test_case(id="SEARCH-010")
    def test_search_by_address(self):
        self._run_full_search_flow("SEARCH-010")

    @test_case(id="SEARCH-011")
    def test_search_by_effective_date(self):
        self._run_full_search_flow("SEARCH-011")

    @test_case(id="SEARCH-012")
    def test_search_by_email(self):
        self._run_full_search_flow("SEARCH-012")

    @test_case(id="SEARCH-013")
    def test_search_by_company_number(self):
        self._run_full_search_flow("SEARCH-013")

    # =========================================================================
    # CATEGORY 2: Combined / Multi-Field Searches
    # =========================================================================

    @test_case(id="SEARCH-014")
    def test_search_combined_name_state(self):
        self._run_full_search_flow("SEARCH-014")

    @test_case(id="SEARCH-015")
    def test_search_combined_agency_state(self):
        self._run_full_search_flow("SEARCH-015")
