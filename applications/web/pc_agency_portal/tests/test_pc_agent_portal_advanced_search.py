from applications.web.pc_agency_portal.tests.base_test import BaseTest
from applications.web.pc_agency_portal.fixtures.login_fixtures import (
    login_to_portal,
)
from core.utils.decorators import test_case
import pytest


class TestPolicyAdvancedSearch(BaseTest):
    persistent_session = True

    @test_case(id="PC-PORTAL-000")
    def test_00_login_and_select_agency(self, login_to_portal):
        """
        Pre-condition: Authenticate into the portal once and select the target agency.
        All subsequent tests will reuse this session.
        """
        self.logger.info("Login pre-condition completed successfully.")

        expected_agency = self.test_data.get("agency") or "01-150-1"
        self.logger.info(f"Selecting target agency: {expected_agency}")

        # 1. Open agency dropdown and select the item
        self.app.agency_code_page.select_an_agency(expected_agency)

        # 2. Get actual selected agency code from the UI before submitting (avoiding page transition issues)
        actual_agency = self.app.agency_code_page.get_selected_agency_code()

        # 3. Assert they match
        assert (
            expected_agency in actual_agency
        ), f"Expected selected agency to contain '{expected_agency}', but got '{actual_agency}'"

        # 4. Submit and proceed to the portal
        self.app.agency_code_page.click_submit_agency_code()
        self.app.home_page.wait_for_login_success()
        self.logger.info("Agency selected and submitted successfully.")

    # ------------------------------- Tests for Advanced Search Page ------------------------------

    @test_case(id="PC-PORTAL-020")
    def test_advanced_search_by_policy_number(self):
        """
        Scenario: Search for a policy using the Policy Number in Advanced Search.
        """
        self.logger.info("Starting advanced search by policy number scenario")
        policy_number = self.test_data.get("policy_number")

        # Open portal and navigate to Advanced Search
        self.app.policy_lookup_advance_page.open_policy_advanced_search()

        # Perform the search
        self.app.policy_lookup_advance_page.type_policy_number(policy_number).click_search_button()

        # Wait for search results
        self.app.policy_lookup_advance_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_policy_number = self.app.policy_lookup_advance_page.get_policy_number()

        assert (
            policy_number == actual_policy_number
        ), f"Expected Policy Number in results to be '{policy_number}', but got '{actual_policy_number}'"

        self.logger.info(
            f"Successfully verified advanced search result for policy: {actual_policy_number}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-021")
    def test_advanced_search_by_insured_name(self):
        """
        Scenario: Search for a policy using the Insured Name in Advanced Search.
        """
        self.logger.info("Starting advanced search by insured name scenario")
        insured_name = self.test_data.get("insured_name")

        # Open portal and navigate to Advanced Search
        self.app.policy_lookup_advance_page.open_policy_advanced_search()

        # Perform the search
        self.app.policy_lookup_advance_page.type_insured_name(insured_name).click_search_button()

        # Wait for search results
        self.app.policy_lookup_advance_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_insured_name = self.app.policy_lookup_advance_page.get_insured_name()

        assert (
            insured_name == actual_insured_name
        ), f"Expected Insured Name in results to be '{insured_name}', but got '{actual_insured_name}'"

        self.logger.info(
            f"Successfully verified advanced search result for Insured Name: {actual_insured_name}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-022")
    def test_advanced_search_by_submission_number(self):
        """
        Scenario: Search for a policy using the Submission Number in Advanced Search.
        """
        self.logger.info("Starting advanced search by submission number scenario")
        submission_number = self.test_data.get("submission_number")

        # Open portal and navigate to Advanced Search
        self.app.policy_lookup_advance_page.open_policy_advanced_search()

        # Perform the search
        self.app.policy_lookup_advance_page.type_submission_number(submission_number).click_search_button()

        # Wait for search results
        self.app.policy_lookup_advance_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_submission_number = self.app.policy_lookup_advance_page.get_submission_number()

        assert (
            submission_number == actual_submission_number
        ), f"Expected Submission Number in results to be '{submission_number}', but got '{actual_submission_number}'"

        self.logger.info(
            f"Successfully verified advanced search result for Submission Number: {actual_submission_number}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-023")
    def test_advanced_search_verify_clear(self):
        """
        Scenario: Fill fields, click Clear, and verify fields are cleared.
        """
        self.logger.info("Starting advanced search clear verification scenario")
        policy_number = self.test_data.get("policy_number")
        insured_name = self.test_data.get("insured_name")
        submission_number = self.test_data.get("submission_number")

        # Open portal and navigate to Advanced Search
        self.app.policy_lookup_advance_page.open_policy_advanced_search()

        # Fill multiple fields
        self.app.policy_lookup_advance_page.type_policy_number(policy_number)
        self.app.policy_lookup_advance_page.type_insured_name(insured_name)
        self.app.policy_lookup_advance_page.type_submission_number(submission_number)

        # Verify values before clear
        val_policy = self.app.policy_lookup_advance_page.element(
            self.app.policy_lookup_advance_page.INP_POLICY_NUMBER
        ).get_attribute("value")
        val_insured = self.app.policy_lookup_advance_page.element(
            self.app.policy_lookup_advance_page.INP_INSURED_NAME
        ).get_attribute("value")
        val_submission = self.app.policy_lookup_advance_page.element(
            self.app.policy_lookup_advance_page.INP_SUBMISSION_NUMBER
        ).get_attribute("value")

        assert val_policy == policy_number, f"Expected policy number to be '{policy_number}' before clear, but got '{val_policy}'"
        assert val_insured == insured_name, f"Expected insured name to be '{insured_name}' before clear, but got '{val_insured}'"
        assert val_submission == submission_number, f"Expected submission number to be '{submission_number}' before clear, but got '{val_submission}'"

        # Click Clear
        self.app.policy_lookup_advance_page.click_clear_button()

        # Verify fields are empty after clear
        val_policy_after = self.app.policy_lookup_advance_page.element(
            self.app.policy_lookup_advance_page.INP_POLICY_NUMBER
        ).get_attribute("value")
        val_insured_after = self.app.policy_lookup_advance_page.element(
            self.app.policy_lookup_advance_page.INP_INSURED_NAME
        ).get_attribute("value")
        val_submission_after = self.app.policy_lookup_advance_page.element(
            self.app.policy_lookup_advance_page.INP_SUBMISSION_NUMBER
        ).get_attribute("value")

        assert val_policy_after == "", f"Expected policy number to be empty after clear, but got '{val_policy_after}'"
        assert val_insured_after == "", f"Expected insured name to be empty after clear, but got '{val_insured_after}'"
        assert val_submission_after == "", f"Expected submission number to be empty after clear, but got '{val_submission_after}'"

        self.logger.info("Successfully verified clear button clears all field values.")
        self.pause(5)
