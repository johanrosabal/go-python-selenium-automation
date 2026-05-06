import pytest
import os
import requests
from core.ui.common.base_app import BaseApp
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager
from core.utils.json_loader import JSONLoader

class BaseAPITest(BaseApp):
    """
    Foundational base class for all API automated test cases.
    Manages the requests session and environment configuration.
    """
    session = None
    
    @property
    def api_base_url(self) -> str:
        """Retrieves the API base URL from configuration."""
        return self.config.get("api.base_url")

    @pytest.fixture(autouse=True)
    def setup_api(self, request):
        """
        Automated Setup and Teardown for API test cases.
        """
        # 1. Resolve Application and Profile (Reuse UI logic if applicable)
        app_name = getattr(self, 'app_name', 'demo')
        app_type = 'api'
        app_path = f"applications/{app_type}/{app_name}"
        
        # 2. Resolve Environment
        env = os.getenv("ENV") or getattr(self, 'profile', 'qa')
        
        # Load configuration
        ConfigManager.load_config(app_path, env)
        
        # 3. Initialize Session
        self.session = requests.Session()
        
        # 4. Resolve Test Data
        func = request.node.function
        test_id = getattr(func, '_test_id', 'N/A')
        self._current_test_id = test_id
        
        self.logger.info(f"🚀 STARTING API TEST: {test_id} | App: {app_name} | Env: {env}")
        
        yield
        
        # Cleanup
        if self.session:
            self.session.close()
            
        self.logger.info(f"🏁 FINISHED API TEST: {test_id}")

    def get_test_data(self, test_id: str = None) -> dict:
        """Utility to load JSON data for the current test context."""
        target_id = test_id if test_id else getattr(self, '_current_test_id', None)
        app_name = getattr(self, 'app_name', 'demo')
        env = os.getenv("ENV") or getattr(self, 'profile', 'qa')
        app_path = f"applications/api/{app_name}"
        
        try:
            return JSONLoader.load_environment_data(app_path, env, target_id)
        except Exception as e:
            self.logger.warning(f"Could not resolve API test data for {target_id}: {e}")
            return {}
