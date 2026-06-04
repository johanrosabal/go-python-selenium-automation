import pytest
from applications.web.pc_agency_portal.app.pc_agency_portal_app import PcAgencyPortalApp

@pytest.fixture
def login_to_portal(request):
    """
    Pytest fixture to perform Microsoft Login and handle Okta MFA.
    It accesses the test instance (self) to use the app and config.
    """
    test_instance = request.instance
    
    # Explicit Type Hinting so your IDE knows exactly what 'app' is
    app: PcAgencyPortalApp = test_instance.app
    
    # Fetch credentials from ConfigManager
    email = test_instance.config.get("credentials.microsoft.email") or ""
    password = test_instance.config.get("credentials.microsoft.password") or ""

    # Open the portal (this will redirect to Microsoft Login if not authenticated)
    app.login_page.open()

    # Check if we are already logged in (Persistent Session)
    if app.home_page.is_logged_in():
        test_instance.logger.info("Session already authenticated. Skipping login steps.")
        return

    # Perform Microsoft Login and handle Okta MFA via UI prompt
    app.login_page.login_microsoft(email, password)

    # Log that we are done with the login phase
    test_instance.logger.info("Waiting for Home Page to become active after login...")
