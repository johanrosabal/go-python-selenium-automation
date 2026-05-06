import allure
from typing import Any
import json

class APIResponse:
    """
    Wrapper for requests.Response to provide fluent assertions and 
    simplified data access.
    """
    def __init__(self, response):
        self._response = response
        self.status_code = response.status_code
        self.reason = response.reason
        self.text = response.text
        self.headers = response.headers
        
    @property
    def body(self) -> Any:
        """Returns the JSON body or raw text if not JSON."""
        try:
            return self._response.json()
        except Exception:
            return self.text

    def assert_status_code(self, expected_code: int):
        """Asserts the HTTP status code."""
        with allure.step(f"Assert status code is {expected_code}"):
            assert self.status_code == expected_code, \
                f"Expected status {expected_code}, but got {self.status_code}. Response: {self.text}"
        return self

    def assert_json_path(self, key: str, expected_value: Any):
        """
        Simple assertion for a key in the JSON body.
        For complex paths, consider using jsonpath-ng.
        """
        with allure.step(f"Assert JSON path '{key}' equals '{expected_value}'"):
            data = self.body
            if not isinstance(data, dict):
                raise AssertionError(f"Response body is not a JSON object: {self.text}")
            
            actual_value = data.get(key)
            assert actual_value == expected_value, \
                f"Expected '{key}' to be '{expected_value}', but got '{actual_value}'"
        return self

    def assert_contains(self, text: str):
        """Asserts that the response body contains the specified text."""
        with allure.step(f"Assert body contains '{text}'"):
            assert text in self.text, f"Expected text '{text}' not found in response body"
        return self

    def __repr__(self):
        return f"<APIResponse [{self.status_code}]>"
