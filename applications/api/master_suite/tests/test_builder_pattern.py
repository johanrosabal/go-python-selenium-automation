import pytest
from core.api.common.base_api_test import BaseAPITest
from applications.api.master_suite.endpoints.master_endpoint import MasterEndpoint
from core.utils.decorators import test_case

class TestBuilderPattern(BaseAPITest):
    """Test suite demonstrating 100% Legacy Builder Style compatibility."""
    app_name = "master_suite"

    @pytest.fixture(autouse=True)
    def setup_master(self):
        self.master = MasterEndpoint(self.session)

    @test_case(id="LEGACY-001", title="Legacy Style: Direct Setters")
    def test_legacy_style(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        payload = {"title": "Legacy", "body": "Style", "userId": 1}
        
        response = self.master.post \
            .set_url(url) \
            .set_json(payload) \
            .add_header("X-Legacy", "True") \
            .send()
            
        response.assert_status_code(201)
        assert response.body["title"] == "Legacy"

    @test_case(id="LEGACY-002", title="Legacy Style: set_endpoint & build_url")
    def test_legacy_endpoint_style(self):
        base = "https://jsonplaceholder.typicode.com"
        
        response = self.master.get \
            .set_url(base) \
            .set_endpoint("/users/{id}/todos") \
            .build_url(id=1) \
            .set_params({"completed": "false"}) \
            .send()
            
        response.assert_status_code(200)
        assert len(response.body) > 0

    @test_case(id="LEGACY-004", title="Full Legacy compatibility: Cookies, Redirects, Verify")
    def test_legacy_full_compat(self):
        # Demonstrating the methods that were missing
        response = self.master.get \
            .set_url("https://httpbin.org/cookies/set/test/value") \
            .set_allow_redirects(True) \
            .set_verify(True) \
            .set_cookies({"session": "builder-test"}) \
            .set_timeout(15) \
            .send()
            
        response.assert_status_code(200)
        # httpbin redirects and then shows the cookies
        assert "builder-test" in str(response.body)
