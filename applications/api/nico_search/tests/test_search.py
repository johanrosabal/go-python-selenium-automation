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

    def _do_search(self, test_id):
        """Helper: loads JSON payload and submits search. Auto-skips on auth/network blocks."""
        data = self.get_test_data(test_id)
        payload = data["data"]["payload"]
        response = self.app.search.search_policies(payload)
        if response.status_code == 401:
            pytest.skip("Invalid/expired token — update qa.yaml.")
        if response.status_code == 403:
            pytest.skip("IP Forbidden — run from authorized network.")
        return response

    def _assert_search_id(self, response):
        """Helper: asserts 201 and extracts the returned GUID."""
        response.assert_status_code(201)
        search_id = response.body.strip()
        assert len(search_id) > 10, f"Expected GUID, got: '{search_id}'"
        return search_id

    # =========================================================================
    # CATEGORY 1: Single-Field Searches
    # =========================================================================

    @test_case(id="SEARCH-001")
    def test_complete_search_flow(self):
        """Full end-to-end via orchestrator: search → GUID → get_results."""
        payload = self.get_test_data()["data"]["payload"]
        search_id, results_response = self.app.search_and_get_results(payload)

        # Skip if auth/IP block is detected during the flow
        if results_response.status_code in [401, 403]:
            pytest.skip("Unauthorized or IP Forbidden.")

        results_response.assert_status_code(200)
        assert isinstance(results_response.body, list), "Expected results body to be a list"

    @test_case(id="SEARCH-002")
    def test_search_by_first_last_name(self):
        self._assert_search_id(self._do_search("SEARCH-002"))

    @test_case(id="SEARCH-003")
    def test_search_by_policy_number(self):
        self._assert_search_id(self._do_search("SEARCH-003"))

    @test_case(id="SEARCH-004")
    def test_search_by_insured_name(self):
        self._assert_search_id(self._do_search("SEARCH-004"))

    @test_case(id="SEARCH-005")
    def test_search_by_phone_number(self):
        self._assert_search_id(self._do_search("SEARCH-005"))

    @test_case(id="SEARCH-006")
    def test_search_by_vin(self):
        self._assert_search_id(self._do_search("SEARCH-006"))

    @test_case(id="SEARCH-007")
    def test_search_by_quote_number(self):
        self._assert_search_id(self._do_search("SEARCH-007"))

    @test_case(id="SEARCH-008")
    def test_search_by_agency_code(self):
        self._assert_search_id(self._do_search("SEARCH-008"))

    @test_case(id="SEARCH-009")
    def test_search_by_policy_state(self):
        self._assert_search_id(self._do_search("SEARCH-009"))

    @test_case(id="SEARCH-010")
    def test_search_by_address(self):
        self._assert_search_id(self._do_search("SEARCH-010"))

    @test_case(id="SEARCH-011")
    def test_search_by_effective_date(self):
        self._assert_search_id(self._do_search("SEARCH-011"))

    @test_case(id="SEARCH-012")
    def test_search_by_email(self):
        self._assert_search_id(self._do_search("SEARCH-012"))

    @test_case(id="SEARCH-013")
    def test_search_by_company_number(self):
        self._assert_search_id(self._do_search("SEARCH-013"))

    # =========================================================================
    # CATEGORY 2: Combined / Multi-Field Searches
    # =========================================================================

    @test_case(id="SEARCH-014")
    def test_search_combined_name_state(self):
        self._assert_search_id(self._do_search("SEARCH-014"))

    @test_case(id="SEARCH-015")
    def test_search_combined_agency_state(self):
        self._assert_search_id(self._do_search("SEARCH-015"))
