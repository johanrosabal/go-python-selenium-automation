import pytest
from core.ui.common.base_test import BaseTest
from applications.web.demo.pages.login_page import LoginPage
from applications.web.demo.utils.decorators import demo
@demo
class TestLogin(BaseTest):
    """
    Test Suite for SauceDemo Login functionality.

    Verifies authentication scenarios using the Page Object Model and 
    fluent interaction patterns.
    """
    def test_valid_login(self):
        """
        Scenario: Login with valid credentials.
        
        Steps:
            1. Open SauceDemo website.
            2. Enter valid username and password.
            3. Submit the login form.
            4. Verify that the user is redirected to the inventory page.
        """
        self.logger.info(f"Starting valid login test on environment: {self.config.get_env()}")
        
        # Access the Singleton LoginPage and perform the sequence using config defaults
        login_page = LoginPage().open() \
                                .login()
        
        # Assertion: Verify successful redirection
        assert login_page.is_login_successful(), "Login redirect failed"
        self.logger.info("Login test completed successfully")
