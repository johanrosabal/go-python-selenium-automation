import pytest
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from applications.web.go_hotel.fixtures.preconditions import logged_in

# Registering global fixtures for the go_hotel project
@pytest.fixture
def app(request):
    """
    Returns the GoHotelApp orchestrator from the test class instance.
    This allows functional fixtures to interact with pages.
    """
    return request.instance.app
