import pytest
from applications.web.busisness_partners_portal.app.busisness_partners_portal_app import BusisnessPartnersPortalApp
from core.utils.base64_utils import decode_base64


@pytest.fixture
def login_to_portal(request):
    """
    Pytest fixture to perform Microsoft Login and handle Okta MFA.
    It accesses the test instance (self) to use the app and config.
    """
    test_instance = request.instance

    # Explicit Type Hinting so your IDE knows exactly what 'app' is
    app: BusisnessPartnersPortalApp = test_instance.app

    # Fetch credentials from ConfigManager
    encoded_email = test_instance.config.get("credentials.microsoft.email") or ""
    email = decode_base64(encoded_email)
    encoded_password = test_instance.config.get("credentials.microsoft.password") or ""
    password = decode_base64(encoded_password)

    # Open the portal (this will redirect to Microsoft Login if not authenticated)
    app.login_page.open()

    # Check if we are already logged in (Persistent Session)
    if app.policy_quote_lookup.is_logged_in():
        test_instance.logger.info("Session already authenticated. Skipping login steps.")
        return

    # Perform Microsoft Login and handle Okta MFA via UI prompt
    app.login_page.login_microsoft(email, password)

    # Wait for the login process (redirections, etc) to finish and Home Page to load
    test_instance.logger.info("Waiting for Home Page to become active after login...")
    app.policy_quote_lookup.wait_for_login_success(timeout=60)
    test_instance.logger.info("Login successful. Proceeding with tests.")
