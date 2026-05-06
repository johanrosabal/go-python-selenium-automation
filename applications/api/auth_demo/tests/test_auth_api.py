import pytest
from core.api.common.base_api_test import BaseAPITest
from applications.api.auth_demo.endpoints.user_auth_endpoint import UserAuthEndpoint
from core.utils.decorators import test_case

class TestAuthAPI(BaseAPITest):
    """Authenticated API Test Suite."""
    app_name = "auth_demo"

    @pytest.fixture(autouse=True)
    def setup_endpoints(self):
        self.user_api = UserAuthEndpoint(self.session)
        # Get token from config (BaseAPITest has access to self.config)
        self.token = self.config.get("api.token")

    @test_case(id="AUTH-001", title="Verify Authenticated List Users")
    def test_list_users_with_auth(self):
        """Verify that we can list users by passing a Bearer token."""
        response = self.user_api.get_users(self.token)
        
        # Validate status code (200 OK)
        response.assert_status_code(200)
        
        # Validate that the response body is a list
        assert isinstance(response.body, list), "Expected a list of users"
        
        print(f"Captured {len(response.body)} users with authenticated request.")

    @test_case(id="AUTH-002", title="Verify Request without Token")
    def test_request_no_token(self):
        """Demonstrate a request without a token."""
        # JSONPlaceholder will still return 200, so we just demonstrate the call
        response = self.user_api.get_users(token="")
        
        response.assert_status_code(200)
        print("Note: JSONPlaceholder ignores tokens, but the 'Authorization' header was sent empty as requested.")
