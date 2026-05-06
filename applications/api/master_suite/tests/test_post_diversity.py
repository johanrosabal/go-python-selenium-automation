import pytest
import io
from core.api.common.base_api_test import BaseAPITest
from applications.api.master_suite.endpoints.master_endpoint import MasterEndpoint
from core.utils.decorators import test_case

class TestPostDiversity(BaseAPITest):
    """Test suite demonstrating the specialized POST methods."""
    app_name = "master_suite"

    @pytest.fixture(autouse=True)
    def setup_master(self):
        self.master = MasterEndpoint(self.session)

    @test_case(id="POST-001", title="POST JSON Body")
    def test_post_json(self):
        payload = {"title": "foo", "body": "bar", "userId": 1}
        # Using with_json explicitly
        response = self.master.post.with_json("https://jsonplaceholder.typicode.com/posts", payload)
        response.assert_status_code(201)
        assert response.body["title"] == "foo"

    @test_case(id="POST-002", title="POST Form Data")
    def test_post_form(self):
        form_data = {"key1": "value1", "key2": "value2"}
        # Using with_form
        response = self.master.post.with_form("https://httpbin.org/post", form_data)
        response.assert_status_code(200)
        # httpbin echoes form data in 'form' key
        assert response.body["form"]["key1"] == "value1"

    @test_case(id="POST-003", title="POST Multipart (Files)")
    def test_post_files(self):
        # Create an in-memory file
        file_content = "Hello World"
        files = {'file': ('test.txt', io.StringIO(file_content))}
        
        # Using with_files
        response = self.master.post.with_files("https://httpbin.org/post", files=files)
        response.assert_status_code(200)
        assert response.body["files"]["file"] == file_content

    @test_case(id="POST-004", title="POST Raw XML")
    def test_post_raw_xml(self):
        xml_content = "<note><to>User</to><from>Antigravity</from><body>Hello</body></note>"
        
        # Using with_raw
        response = self.master.post.with_raw(
            "https://httpbin.org/post", 
            data=xml_content, 
            content_type="application/xml"
        )
        response.assert_status_code(200)
        assert response.body["data"] == xml_content
