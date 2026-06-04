from applications.web.pc_agency_portal.tests.base_test import BaseTest
from applications.web.pc_agency_portal.tests.fixtures.login_fixtures import (
    login_to_portal,
)
from core.utils.decorators import test_case
import pytest


class TestHomePage(BaseTest):

    @test_case(id="PC-PORTAL-001")
    def test_search_by_policy_number(self, login_to_portal):
        """
        Scenario: Search for a policy using the Policy Number tab.
        """
        self.logger.info("Starting policy number search scenario")
        policy_number = self._current_test_data.get("policy_number")

        # Perform the search
        self.app.home_page.search_for_policy_number(policy_number)

        # Wait for loading spinner and table to load
        self.app.home_page.wait_for_search_results(timeout=60)

        # Verify the search results
        actual_policy_number = self.app.home_page.get_first_policy_number()

        assert (
            policy_number == actual_policy_number
        ), f"Expected Policy Number in results to be '{policy_number}', but got '{actual_policy_number}'"

        self.logger.info(
            f"Successfully verified search result for policy: {actual_policy_number}"
        )

        self.pause(5)
