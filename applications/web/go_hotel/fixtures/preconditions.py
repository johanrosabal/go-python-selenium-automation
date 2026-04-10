import pytest
import allure
from applications.web.go_hotel.app.go_hotel_app import GoHotelApp

@pytest.fixture
def logged_in(request):
    """
    Precondition: Ensure the user is logged in before the test starts.
    If already logged in (persistent session), it skips the login steps.
    """
    # Adding type hint to restore IntelliSense (Go To Definition, Autocomplete)
    app: GoHotelApp = request.instance.app
    
    if app.login_page.is_login_not_logged():
        with allure.step("Precondition: Performing automatic login"):
            app.login_page.wait_for_page_load().login()
            # Navigation is accessed through a page object
            app.dashboard_page.navigation.wait_url_contains("dashboard")
            
    return app
