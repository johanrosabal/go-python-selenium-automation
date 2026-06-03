from applications.web.pc_agency_portal.tests.base_test import BaseTest


class TestPortal(BaseTest):
    def test_search_by_policy_number(self):
        """
        Scenario: Search for a policy using the Policy Number tab.
        """
        self.logger.info("Starting policy number search scenario")
        policy_number = "01APT04875901"  # Mock policy number

        # Fetch credentials from ConfigManager
        email = self.config.get("credentials.microsoft.email") or ""
        password = self.config.get("credentials.microsoft.password") or ""

        # Open the portal (this will redirect to Microsoft Login)
        self.app.login_page.open()

        # Perform Microsoft Login and handle Okta MFA via UI prompt
        self.app.login_page.login_microsoft(email, password)

        # Wait for Home Page to load after successful login (you might need to adjust this explicit wait later)
        self.logger.info("Waiting for Home Page to become active after login...")

        # Perform the search
        self.app.home_page.search_for_policy_number(policy_number)
        
        # Wait for loading spinner and table to load
        self.app.home_page.wait_for_search_results(timeout=15)

        # Verify the search results
        actual_policy_number = self.app.home_page.get_first_policy_number()
        
        self.assertEqual(
            policy_number, 
            actual_policy_number, 
            f"Expected Policy Number in results to be '{policy_number}', but got '{actual_policy_number}'"
        )
        
        self.logger.info(f"Successfully verified search result for policy: {actual_policy_number}")
