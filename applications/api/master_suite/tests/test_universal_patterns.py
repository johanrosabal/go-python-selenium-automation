import pytest
from core.api.common.base_api_test import BaseAPITest
from applications.api.master_suite.endpoints.master_endpoint import MasterEndpoint
from core.utils.decorators import test_case

class TestUniversalPatterns(BaseAPITest):
    """Test suite verifying standardized patterns across all HTTP methods."""
    app_name = "master_suite"

    @pytest.fixture(autouse=True)
    def setup_master(self):
        self.master = MasterEndpoint(self.session)

    @test_case(id="UNI-001", title="GET with Specialized Params")
    def test_get_specialized(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        response = self.master.get.with_params(url, params={"userId": 1})
        response.assert_status_code(200)
        assert response.body[0]["userId"] == 1

    @test_case(id="UNI-002", title="PUT with Specialized JSON")
    def test_put_specialized(self):
        url = "https://jsonplaceholder.typicode.com/posts/1"
        payload = {"id": 1, "title": "Updated", "body": "Standardized", "userId": 1}
        response = self.master.put.with_json(url, payload)
        response.assert_status_code(200)
        assert response.body["title"] == "Updated"

    @test_case(id="UNI-003", title="PATCH with Specialized Form")
    def test_patch_specialized(self):
        url = "https://httpbin.org/patch"
        form_data = {"status": "patched"}
        response = self.master.patch.with_form(url, form_data)
        response.assert_status_code(200)
        assert response.body["form"]["status"] == "patched"

    @test_case(id="UNI-004", title="DELETE with Builder Pattern")
    def test_delete_builder(self):
        url = "https://jsonplaceholder.typicode.com/posts/1"
        # Using the builder pattern for DELETE
        response = self.master.delete.builder() \
            .set_url(url) \
            .add_header("X-Reason", "Cleanup") \
            .send()
        response.assert_status_code(200)
