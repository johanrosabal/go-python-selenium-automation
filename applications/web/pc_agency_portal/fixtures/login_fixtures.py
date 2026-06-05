import pytest
from applications.web.pc_agency_portal.app.pc_agency_portal_app import PcAgencyPortalApp
from core.utils.base64_utils import decode_base64

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
    encoded_email = test_instance.config.get("credentials.microsoft.email") or ""
    email = decode_base64(encoded_email)
    encoded_password = test_instance.config.get("credentials.microsoft.password") or ""
    password = decode_base64(encoded_password)

    # Open the portal (this will redirect to Microsoft Login if not authenticated)
    app.login_page.open()

    # Check if we are already logged in (Persistent Session)
    if app.home_page.is_logged_in():
        test_instance.logger.info("Session already authenticated. Skipping login steps.")
        return

    # Perform Microsoft Login and handle Okta MFA via UI prompt
    app.login_page.login_microsoft(email, password)

    # Wait for the login process (redirections, etc) to finish and load either the Agency Code page or the Home Page
    test_instance.logger.info("Waiting for either Agency Code page or Home Page to become active after login...")
    import time
    timeout = 60
    start_time = time.time()
    on_agency_page = False
    on_home_page = False
    
    while time.time() - start_time < timeout:
        if app.agency_code_page.is_visible():
            on_agency_page = True
            test_instance.logger.info("Redirected to Agency Code Page.")
            break
        if app.home_page.is_logged_in():
            on_home_page = True
            test_instance.logger.info("Redirected directly to Home Page.")
            break
        time.sleep(1)
        
    if not on_agency_page and not on_home_page:
        raise TimeoutError("Timed out waiting for either Agency Code page or Home Page to load.")

    # Determine if this is the explicit agency selection test case
    is_select_agency_test = "select_agency" in request.node.name

    if on_agency_page:
        if is_select_agency_test:
            test_instance.logger.info("On Agency Code page. Skipping auto-selection because this is the explicit agency selection test case.")
        else:
            # Auto-select agency for other tests to proceed to the Home Page
            agency = test_instance.test_data.get("agency") or "Berkshire Hathaway Homestate CompaniesOmahaNE"
            test_instance.logger.info(f"Auto-selecting agency code: {agency}")
            app.agency_code_page.select_an_agency(agency)
            
            # Wait for the Home Page to load
            test_instance.logger.info("Waiting for Home Page to become active after agency selection...")
            app.home_page.wait_for_login_success(timeout=30)
            test_instance.logger.info("Login and agency selection successful. Proceeding with tests.")
    else:
        test_instance.logger.info("Login successful (already on Home Page). Proceeding with tests.")
