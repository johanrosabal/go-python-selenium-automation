from applications.web.busisness_partners_portal.tests.base_test import BaseTest
from applications.web.busisness_partners_portal.fixtures.login_fixtures import (
    login_to_portal,
)
from core.utils.decorators import test_case
import pytest


class TestPolicyAdvanceSearch(BaseTest):
    persistent_session = True

    @test_case(id="PC-PORTAL-000")
    def test_00_login(self, login_to_portal):
        """
        Pre-condition: Authenticate into the portal once.
        All subsequent tests will reuse this session.
        """
        self.logger.info("Login pre-condition completed successfully.")
        self.app.policy_quote_lookup.click_accept_cookies()

    # ------------------------------- Tests for Policy Advanced Search ------------------------------

    @test_case(id="PC-PORTAL-020")
    def test_advance_search_by_policy_number(self):
        """
        Scenario: Search for a policy using the Policy Number in Advanced Search.
        """
        self.logger.info("Starting advanced search by policy number scenario")
        policy_number = self.test_data.get("policy_number")

        # Open portal and click Advanced Search link
        self.app.policy_quote_lookup.open_policy_quote_lookup()
        self.app.policy_quote_lookup.click_advanced_search_link()

        # Perform the search
        self.app.policy_advance_search_page.type_policy_number(policy_number).click_search_button()

        # Wait for search results
        self.app.policy_advance_search_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_policy_number = self.app.policy_advance_search_page.get_policy_number()

        assert (
            policy_number == actual_policy_number
        ), f"Expected Policy Number in results to be '{policy_number}', but got '{actual_policy_number}'"

        self.logger.info(
            f"Successfully verified advanced search result for policy: {actual_policy_number}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-021")
    def test_advance_search_by_insured_name(self):
        """
        Scenario: Search for a policy using the Insured Name in Advanced Search.
        """
        self.logger.info("Starting advanced search by insured name scenario")
        insured_name = self.test_data.get("insured_name")

        # Open portal and click Advanced Search link
        self.app.policy_quote_lookup.open_policy_quote_lookup()
        self.app.policy_quote_lookup.click_advanced_search_link()

        # Perform the search
        self.app.policy_advance_search_page.type_insured_name(insured_name).click_search_button()

        # Wait for search results
        self.app.policy_advance_search_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_insured_name = self.app.policy_advance_search_page.get_insured_name()

        assert (
            insured_name == actual_insured_name
        ), f"Expected Insured Name in results to be '{insured_name}', but got '{actual_insured_name}'"

        self.logger.info(
            f"Successfully verified advanced search result for Insured Name: {actual_insured_name}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-022")
    def test_advance_search_by_quote_number(self):
        """
        Scenario: Search for a policy using the Quote Number in Advanced Search.
        """
        self.logger.info("Starting advanced search by quote number scenario")
        quote_number = self.test_data.get("quote_number")

        # Open portal and click Advanced Search link
        self.app.policy_quote_lookup.open_policy_quote_lookup()
        self.app.policy_quote_lookup.click_advanced_search_link()

        # Perform the search
        self.app.policy_advance_search_page.type_quote_number(quote_number).click_search_button()

        # Wait for search results
        self.app.policy_advance_search_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_quote_number = self.app.policy_advance_search_page.get_quote_number()

        assert (
            quote_number == actual_quote_number
        ), f"Expected Quote Number in results to be '{quote_number}', but got '{actual_quote_number}'"

        self.logger.info(
            f"Successfully verified advanced search result for Quote Number: {actual_quote_number}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-023")
    def test_advance_search_verify_clear(self):
        """
        Scenario: Fill fields, click Clear, and verify fields are cleared.
        """
        self.logger.info("Starting advanced search clear verification scenario")
        policy_number = self.test_data.get("policy_number")
        insured_name = self.test_data.get("insured_name")
        quote_number = self.test_data.get("quote_number")

        # Open portal and click Advanced Search link
        self.app.policy_quote_lookup.open_policy_quote_lookup()
        self.app.policy_quote_lookup.click_advanced_search_link()

        # Fill multiple fields
        self.app.policy_advance_search_page.type_policy_number(policy_number)
        self.app.policy_advance_search_page.type_insured_name(insured_name)
        self.app.policy_advance_search_page.type_quote_number(quote_number)

        # Verify values before clear
        val_policy = self.app.policy_advance_search_page.element(
            self.app.policy_advance_search_page.INP_POLICY_NUMBER
        ).get_attribute("value")
        val_insured = self.app.policy_advance_search_page.element(
            self.app.policy_advance_search_page.INP_INSURED_NAME
        ).get_attribute("value")
        val_quote = self.app.policy_advance_search_page.element(
            self.app.policy_advance_search_page.INP_QUOTE_NUMBER
        ).get_attribute("value")

        assert val_policy == policy_number, f"Expected policy number to be '{policy_number}' before clear, but got '{val_policy}'"
        assert val_insured == insured_name, f"Expected insured name to be '{insured_name}' before clear, but got '{val_insured}'"
        assert val_quote == quote_number, f"Expected quote number to be '{quote_number}' before clear, but got '{val_quote}'"

        # Click Clear
        self.app.policy_advance_search_page.click_clear_button()

        # Verify fields are empty after clear
        val_policy_after = self.app.policy_advance_search_page.element(
            self.app.policy_advance_search_page.INP_POLICY_NUMBER
        ).get_attribute("value")
        val_insured_after = self.app.policy_advance_search_page.element(
            self.app.policy_advance_search_page.INP_INSURED_NAME
        ).get_attribute("value")
        val_quote_after = self.app.policy_advance_search_page.element(
            self.app.policy_advance_search_page.INP_QUOTE_NUMBER
        ).get_attribute("value")

        assert val_policy_after == "", f"Expected policy number to be empty after clear, but got '{val_policy_after}'"
        assert val_insured_after == "", f"Expected insured name to be empty after clear, but got '{val_insured_after}'"
        assert val_quote_after == "", f"Expected quote number to be empty after clear, but got '{val_quote_after}'"

        self.logger.info("Successfully verified clear button clears all field values.")
        self.pause(5)
