from core.ui.common.base_test import BaseTest
from applications.web.go_hotel.config.decorators.app_decorators import go_hotel
from applications.web.go_hotel.app.go_hotel_app import GoHotelApp
from core.utils.decorators import test_case

@go_hotel
class TestLogin(BaseTest):
    app: GoHotelApp  # Type hint to restore IntelliSense (Pylance)

    @test_case(id="HOTEL-001")
    def test_successful_login(self):
        # Open base url from config + login route using the Orchestrator
        self.app.login_page.wait_for_page_load()
        
        # Uses config default username/password if empty
        self.app.login_page.login()
        
        # Verify successful login
        assert self.app.login_page.is_login_successful(), "Login failed: User was not redirected from login page"
        self.app.screenshot(name="Successful Login")

    @test_case(id="HOTEL-002")
    def test_failed_login_invalid_password(self):
        test_data = self.get_test_data()
        # Open base url from config + login route using the Orchestrator
        self.app.login_page.wait_for_page_load()
        
        # Provide invalid password explicitly (skip success sync to avoid timeout)
        self.app.login_page.login(password=test_data['password'], wait_success=False)
        
        # Verify login wasn't successful
        assert self.app.login_page.is_login_not_logged(), "Login succeeded with wrong password, this should not happen"
        self.app.screenshot(name="Failed Login")

