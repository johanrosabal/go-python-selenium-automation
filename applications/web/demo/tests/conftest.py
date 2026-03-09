import pytest
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from applications.web.demo.fixtures.preconditions import logged_in_session

# Registering global fixtures for this project
@pytest.fixture
def app(request):
    """
    Returns the DemoApp orchestrator from the test class instance.
    This allows functional fixtures to interact with pages.
    """
    return request.instance.app
