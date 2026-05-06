import pytest
from core.api.common.base_api_test import BaseAPITest
from applications.api.params_demo.endpoints.social_endpoint import SocialEndpoint
from core.utils.decorators import test_case

class TestParamsAPI(BaseAPITest):
    """Test suite for URL Parameters diversity."""
    app_name = "params_demo"

    @pytest.fixture(autouse=True)
    def setup_endpoints(self):
        self.social_api = SocialEndpoint(self.session)

    @test_case(id="PARAM-001", title="Verify Path Parameter (Single Post)")
    def test_path_parameter(self):
        """Verify fetching a specific post using its ID in the URL path."""
        post_id = 1
        response = self.social_api.get_post(post_id)
        
        response.assert_status_code(200)
        assert response.body["id"] == post_id
        print(f"Successfully retrieved post {post_id} via path parameter.")

    @test_case(id="PARAM-002", title="Verify Query Parameter (Filtered Comments)")
    def test_query_parameter(self):
        """Verify fetching comments filtered by postId using query parameters."""
        post_id = 1
        response = self.social_api.get_comments(post_id)
        
        response.assert_status_code(200)
        assert isinstance(response.body, list)
        # Verify all comments belong to the requested post
        for comment in response.body:
            assert comment["postId"] == post_id
            
        print(f"Successfully retrieved {len(response.body)} comments for post {post_id} via query parameter.")

    @test_case(id="PARAM-003", title="Verify Nested Path Parameter (User Albums)")
    def test_nested_path_parameter(self):
        """Verify fetching a user's albums using nested path parameters."""
        user_id = 1
        response = self.social_api.get_user_albums(user_id)
        
        response.assert_status_code(200)
        assert isinstance(response.body, list)
        print(f"Successfully retrieved {len(response.body)} albums for user {user_id} via nested path.")
