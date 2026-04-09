import pytest
import allure

@pytest.fixture
def logged_in_session(app):
    """
    Precondition: Ensure the user is logged in before the test starts.
    Checks if already logged in, otherwise uses config credentials.
    """
    if not app.login_page.is_login_successful():
        with allure.step(f"Precondition: Login as {app.username}"):
            app.login_page.open().login(app.username, app.password)
            
    return app
