import functools
import allure
from core.utils.json_loader import JSONLoader
from core.utils.config_manager import ConfigManager

def test_case(id: str):
    """
    Custom decorator to link a test method with its JSON metadata and Allure report.
    Loads metadata at decoration time to make it available for fixtures.
    """
    # 1. Resolve Application Path (for now demo)
    app_path = 'applications/web/demo' 
    
    # 2. Pre-load Metadata (Decoration time)
    metadata = {}
    try:
        content = JSONLoader.load_test_data(app_path, id)
        metadata = content.get("tests", {})
    except Exception as e:
        print(f"Warning: Could not load metadata for @test_case(id='{id}') at decoration time: {e}")

    def decorator(func):
        # Attach metadata for early access (e.g., fixtures)
        func._test_id = id
        func._test_title = metadata.get("title", func.__name__)
        func._test_metadata = metadata

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # args[0] is 'self' (the test class instance)
            test_instance = args[0]
            
            # Apply Allure Metadata Dynamically
            allure.dynamic.title(func._test_title)
            allure.dynamic.description(metadata.get("description", ""))
            allure.dynamic.severity(metadata.get("severity", "normal").lower())
            allure.dynamic.feature(metadata.get("feature", "Default Feature"))
            
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
            tags = metadata.get("tag", [])
            for tag in tags:
                allure.dynamic.tag(tag)
            
            # Attach Data to 'self' for easy access
            test_instance._current_test_data = metadata.get("data", {})
            test_instance._current_test_id = id
            test_instance._current_test_title = func._test_title

            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Tell pytest this function is NOT a test itself
test_case.__test__ = False
