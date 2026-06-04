from applications.web.pc_agency_portal.tests.base_test import BaseTest
from applications.web.pc_agency_portal.fixtures.login_fixtures import (
    login_to_portal,
)
from core.utils.decorators import test_case
import pytest


class TestHomePage(BaseTest):
    persistent_session = True

    def test_00_login(self, login_to_portal):
        """
        Pre-condition: Authenticate into the portal once.
        All subsequent tests will reuse this session.
        """
        self.logger.info("Login pre-condition completed successfully.")

    @test_case(id="PC-PORTAL-001")
    def test_search_by_policy_number(self):
        """
        Scenario: Search for a policy using the Policy Number tab.
        """
        self.logger.info("Starting policy number search scenario")
        policy_number = self._current_test_data.get("policy_number")

        # Ensure we are on the Home Page
        self.app.home_page.open_home_page()

        # Perform the search
        self.app.home_page.search_for_policy_number(policy_number)

        # Wait for loading spinner and table to load
        self.app.home_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_policy_number = self.app.home_page.get_policy_number()

        assert (
            policy_number == actual_policy_number
        ), f"Expected Policy Number in results to be '{policy_number}', but got '{actual_policy_number}'"

        self.logger.info(
            f"Successfully verified search result for policy: {actual_policy_number}"
        )

        self.pause(5)

    @test_case(id="PC-PORTAL-002")
    def test_search_by_insured_name(self):
        """
        Scenario: Search for a policy using the Insured Name tab.
        """
        self.logger.info("Starting insured name search scenario")
        insured_name = self._current_test_data.get("insured_name")

        # Ensure we are on the Home Page
        self.app.home_page.open_home_page()

        # Perform the search
        self.app.home_page.search_for_insured_name(insured_name)

        # Wait for loading spinner and table to load
        self.app.home_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_insured_name = self.app.home_page.get_insured_name()

        assert (
            insured_name == actual_insured_name
        ), f"Expected Insured Name in results to be '{insured_name}', but got '{actual_insured_name}'"

        self.logger.info(
            f"Successfully verified search result for Insured Name: {actual_insured_name}"
        )
        self.pause(5)

    @test_case(id="PC-PORTAL-003")
    def test_search_by_submission_number(self):
        """
        Scenario: Search for a policy using the Submission Number tab.
        """
        self.logger.info("Starting submission number search scenario")
        submission_number = self._current_test_data.get("submission_number")

        # Ensure we are on the Home Page
        self.app.home_page.open_home_page()

        # Perform the search
        self.app.home_page.search_for_submission_number(submission_number)

        # Wait for loading spinner and table to load
        self.app.home_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_submission_number = self.app.home_page.get_submission_number()

        assert (
            submission_number == actual_submission_number
        ), f"Expected Submission Number in results to be '{submission_number}', but got '{actual_submission_number}'"

        self.logger.info(
            f"Successfully verified search result for Submission Number: {actual_submission_number}"
        )
        self.pause(5)
