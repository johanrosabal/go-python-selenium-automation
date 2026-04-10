import functools
import allure
from core.utils.json_loader import JSONLoader
from core.utils.config_manager import ConfigManager

import os

def test_case(id: str, json_file: str = None, title: str = None, description: str = None, feature: str = None, story: str = None, severity: str = None, skip: bool = False, skip_reason: str = None):
    """
    Custom decorator to link a test method with its JSON metadata and Allure report.
    Resolves metadata dynamically using execution variables (app_name, app_type).
    """
    def decorator(func):
        # Apply native pytest skip mark if requested
        if skip:
            import pytest
            reason = skip_reason or f"Test Case {id} skipped via @test_case decorator."
            func = pytest.mark.skip(reason=reason)(func)

        # Attach basic metadata for early access by Pytest setup fixtures
        func._test_id = id
        func._test_json_file = json_file
        func._test_arg_title = title
        func._test_arg_description = description
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # args[0] is 'self' (the test class instance)
            test_instance = args[0]
            
            # Consume the dynamically loaded metadata pre-attached by BaseTest setup
            metadata = getattr(func, '_test_metadata', {})
            
            # Use the resolved values from BaseTest (Priority: JSON -> Args -> Default)
            _title = getattr(func, '_test_title', title or func.__name__)
            _desc = getattr(func, '_test_description', description or "")

            # Apply Allure Metadata Dynamically
            allure.dynamic.title(_title)
            
            if _desc:
                allure.dynamic.description(_desc)
                
            _sev = severity or metadata.get("severity", "normal")
            allure.dynamic.severity(_sev.lower())
            
            _feat = feature or metadata.get("feature", "Default Feature")
            allure.dynamic.feature(_feat)
            
            _story = story or metadata.get("story")
            if _story:
                allure.dynamic.story(_story)
            
            # Link TMS (Dynamic)
            tms_base_url = ConfigManager.get("tms")
            if tms_base_url:
                tms_link = f"{tms_base_url.rstrip('/')}/{id}"
                allure.dynamic.link(tms_link, name=f"TMS Case: {id}")
            
            # Link Jira/External (Override from JSON if present)
            link = metadata.get("link", {})
            if link.get("url"):
                allure.dynamic.link(link.get("url"), name=link.get("name", id))
            
            # Tags
            _tags = metadata.get("tag", [])
            for tag in _tags:
                allure.dynamic.tag(tag)
            
            # Attach Data to 'self' for easy access
            test_instance._current_test_data = metadata.get("data", {})
            test_instance._current_test_id = id
            test_instance._current_test_title = _title

            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Tell pytest this function is NOT a test itself
test_case.__test__ = False
