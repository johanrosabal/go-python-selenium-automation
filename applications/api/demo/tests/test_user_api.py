from core.api.common.base_api_test import BaseAPITest
from applications.api.demo.endpoints.user_endpoint import UserEndpoint
import pytest

class TestUserAPI(BaseAPITest):
    app_name = "demo"
    
    def test_list_users(self):
        """Verify that users can be listed via GET."""
        users_api = UserEndpoint(self.session)
        
        response = users_api.get_users()
        
        response.assert_status_code(200)
        
        assert isinstance(response.body, list)
        assert len(response.body) > 0

    def test_create_user_demo(self):
        """Verify that a user can be created via POST."""
        users_api = UserEndpoint(self.session)
        
        response = users_api.create_user(name="morpheus", job="leader")
        
        response.assert_status_code(201) \
                .assert_json_path("name", "morpheus") \
                .assert_json_path("job", "leader")
