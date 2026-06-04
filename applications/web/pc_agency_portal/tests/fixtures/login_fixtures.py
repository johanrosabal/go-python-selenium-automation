import pytest

@pytest.fixture
def login_to_portal(request):
    """
    Pytest fixture to perform Microsoft Login and handle Okta MFA.
    It accesses the test instance (self) to use the app and config.
    """
    test_instance = request.instance
    
    # Fetch credentials from ConfigManager
    email = test_instance.config.get("credentials.microsoft.email") or ""
    password = test_instance.config.get("credentials.microsoft.password") or ""

    # Open the portal (this will redirect to Microsoft Login)
    test_instance.app.login_page.open()

    # Perform Microsoft Login and handle Okta MFA via UI prompt
    test_instance.app.login_page.login_microsoft(email, password)

    # Log that we are done with the login phase
    test_instance.logger.info("Waiting for Home Page to become active after login...")
