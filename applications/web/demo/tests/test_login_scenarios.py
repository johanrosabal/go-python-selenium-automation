from core.ui.common.base_test import BaseTest
from applications.web.demo.pages.login_page import LoginPage
from applications.web.demo.pages.inventory_page import InventoryPage
from core.utils.decorators import test_case
from applications.web.demo.utils.decorators import demo

@demo
class TestLoginScenarios(BaseTest):
    """
    Expanded Test Suite for SauceDemo authentication and navigation.
    """

    @test_case(id="CT-LOGIN-003")
    def test_valid_login_and_logout(self):
        """Valid login followed by a logout."""
        
        # 1. Login using config defaults
        login_page = LoginPage().open() \
                                .login()
        
        # Verify successful login using the new method
        assert login_page.is_login_successful(), "Login was not successful"
        
        inventory = InventoryPage()
        
        # 2. Logout
        inventory.logout()
        # Verify we are back on the login page
        self.logger.info(f"Actual URL after logout: {self.get_current_url()}")
        assert self.get_current_url().rstrip("/") == self.base_url.rstrip("/"), \
            f"Logout redirect failed. Expected {self.base_url} but got {self.get_current_url()}"

    @test_case(id="CT-LOGIN-001")
    def test_invalid_login(self):
        """Attempt login with incorrect credentials."""
        
        # Load data automatically from decorator cache
        test_data = self.get_data_for_test()
        
        invalid_user = test_data.get("username")
        invalid_pass = test_data.get("password")
        expected_msg = self.config.get(test_data.get("error_key"))
        
        login_page = LoginPage().open_relative("/")
        login_page.login(invalid_user, invalid_pass)
        
        assert login_page.get_error_message() == expected_msg

    @test_case(id="CT-LOGIN-002")
    def test_locked_out_user(self):
        """Attempt login with a locked out user."""
        
        # Load data automatically from decorator cache
        test_data = self.get_data_for_test()
        
        locked_user = test_data.get("username")
        locked_pass = test_data.get("password")
        expected_msg = self.config.get(test_data.get("error_key"))
        
        login_page = LoginPage().open_relative("/")
        login_page.login(locked_user, locked_pass)
        
        assert login_page.get_error_message() == expected_msg
