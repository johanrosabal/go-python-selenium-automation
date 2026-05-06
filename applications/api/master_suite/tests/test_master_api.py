import pytest
import time
from core.api.common.base_api_test import BaseAPITest
from applications.api.master_suite.endpoints.master_endpoint import MasterEndpoint
from core.utils.decorators import test_case
from core.utils.config_manager import ConfigManager

class TestMasterAPI(BaseAPITest):
    """The Ultimate API Master Suite with diverse scenarios."""
    app_name = "master_suite"

    @pytest.fixture(autouse=True)
    def setup_master(self):
        self.master = MasterEndpoint(self.session)
        self.sla = ConfigManager.get("api.sla_limit_ms")

    # --- CATEGORY 1: CRUD Operations ---

    @test_case(id="CRUD-001", title="Create Resource (POST)")
    def test_create_user(self):
        response = self.master.create_user("Test Resource", "Lead")
        response.assert_status_code(201)
        # JSONPlaceholder returns the object with an id: 101
        assert "id" in response.body

    @test_case(id="CRUD-002", title="Read User (GET)")
    def test_read_user(self):
        response = self.master.get_user_by_id(1)
        response.assert_status_code(200)
        assert response.body["id"] == 1

    @test_case(id="CRUD-003", title="Update User Full (PUT)")
    def test_update_user(self):
        response = self.master.update_user(2, "John Smith", "Manager")
        response.assert_status_code(200)
        assert response.body["name"] == "John Smith"

    @test_case(id="CRUD-004", title="Update User Partial (PATCH)")
    def test_patch_user(self):
        response = self.master.patch_user(2, "Architect")
        response.assert_status_code(200)
        assert response.body["job"] == "Architect"

    @test_case(id="CRUD-005", title="Delete Resource (DELETE)")
    def test_delete_user(self):
        response = self.master.delete_user(1)
        response.assert_status_code(200) # JSONPlaceholder returns 200

    # --- CATEGORY 2: Error Handling ---

    @test_case(id="ERR-001", title="Handle Not Found (404)")
    def test_404_error(self):
        response = self.master.force_error(404)
        response.assert_status_code(404)

    @test_case(id="ERR-002", title="Handle Unauthorized (401)")
    def test_401_error(self):
        response = self.master.force_error(401)
        response.assert_status_code(401)

    # --- CATEGORY 3: Headers & Metadata ---

    @test_case(id="META-001", title="Custom Headers Validation")
    def test_custom_headers(self):
        headers = {"X-Test-Mode": "True", "Accept-Language": "es-ES"}
        response = self.master.get_with_custom_headers(headers)
        response.assert_status_code(200)
        # JSONPlaceholder returns the original post, but our logger captures the headers sent

    # --- CATEGORY 4: Complex Parameters ---

    @test_case(id="PARAM-001", title="Multiple Query Parameters")
    def test_multiple_params(self):
        response = self.master.get_filtered_comments(post_id=1, limit=3)
        response.assert_status_code(200)
        assert len(response.body) == 3

    # --- CATEGORY 5: Performance & SLA ---

    @test_case(id="PERF-001", title="Response Time SLA Check")
    def test_response_time_sla(self):
        start_time = time.time()
        response = self.master.get_users()
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        print(f"Response received in {duration_ms:.2f}ms (Limit: {self.sla}ms)")
        
        response.assert_status_code(200)
        assert duration_ms < self.sla, f"SLA Violation: {duration_ms:.2f}ms > {self.sla}ms"
