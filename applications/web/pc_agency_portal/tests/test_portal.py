from applications.web.pc_agency_portal.tests.base_test import BaseTest

class TestPortal(BaseTest):
    def test_search_by_policy_number(self):
        """
        Scenario: Search for a policy using the Policy Number tab.
        """
        self.logger.info("Starting policy number search scenario")
        policy_number = "123456789" # Mock policy number
        
        # Fetch credentials from ConfigManager
        email = self.config.get("credentials.microsoft.email")
        password = self.config.get("credentials.microsoft.password")
        
        # Open the portal (this will redirect to Microsoft Login)
        self.app.login_page.open()
        
        # Perform Microsoft Login and handle Okta MFA via UI prompt
        self.app.login_page.login_microsoft(email, password)
        
        # Wait for Home Page to load after successful login (you might need to adjust this explicit wait later)
        self.logger.info("Waiting for Home Page to become active after login...")
        
        # Perform the search
        self.app.home_page.search_for_policy_number(policy_number)
        
        # TODO: Add assertions to verify the search results once the result page is implemented
        self.logger.info(f"Successfully performed search for policy: {policy_number}")
