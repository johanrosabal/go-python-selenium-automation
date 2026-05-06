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
        
        # 4. Initialize App Orchestrator (mirrors the UI BaseTest pattern)
        #    Maps app_name -> Client class, instantiated automatically as self.app
        self.app = self._resolve_app_client(app_name, env)
        
        # 4. Resolve Test Data & inject JSON metadata into func (mirrors BaseTest.setup)
        func = request.node.function
        test_id = getattr(func, '_test_id', 'N/A')
        self._current_test_id = test_id
        self._current_test_data = {}

        arg_title = getattr(func, '_test_arg_title', None)
        arg_desc  = getattr(func, '_test_arg_description', None)

        try:
            env_content = JSONLoader.load_environment_data(app_path, env, test_id)
            if env_content:
                metadata = env_content.get("tests", {})
                self._current_test_data  = metadata.get("data", {})
                func._test_metadata      = metadata          # consumed by @test_case wrapper
                func._test_title         = metadata.get("title")      or arg_title or func.__name__
                func._test_description   = metadata.get("description") or arg_desc  or ""
        except Exception:
            pass

        test_title = getattr(func, '_test_title', arg_title or test_id)
        self.logger.info(f"🚀 STARTING API TEST: {test_id} - {test_title} | App: {app_name} | Env: {env}")
        
        yield
        
        # Cleanup
        if self.session:
            self.session.close()
            
        self.logger.info(f"🏁 FINISHED API TEST: {test_id}")

    def _resolve_app_client(self, app_name: str, env: str):
        """
        Auto-discovers and loads the App Orchestrator by convention.

        Convention: if applications/api/{app_name}/client.py exists,
        it will be imported and instantiated automatically — no registration needed.

        The first class found in the module is used. Constructor is called with
        (session, config) if it accepts config, otherwise with (session,) alone.
        """
        import importlib
        import inspect

        module_path = f"applications.api.{app_name}.client"
        config = ConfigManager.get("api") or {}

        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            self.logger.warning(
                f"No client.py found for app '{app_name}' "
                f"(looked for {module_path}). self.app = None."
            )
            return None

        # Find the first class defined in the module
        client_class = None
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_path:
                client_class = obj
                break

        if not client_class:
            self.logger.warning(f"client.py found for '{app_name}' but contains no class.")
            return None

        # Try instantiating with (session, config), fall back to (session,)
        try:
            sig = inspect.signature(client_class.__init__)
            params = list(sig.parameters.keys())  # ['self', 'session', 'config', ...]
            if len(params) >= 3:  # has at least session + config
                instance = client_class(self.session, config)
            else:
                instance = client_class(self.session)
            self.logger.info(f"✅ App client loaded: {client_class.__name__} for '{app_name}'")
            return instance
        except Exception as e:
            self.logger.error(f"Failed to instantiate client for '{app_name}': {e}")
            return None


    def get_test_data(self, test_id: str = None) -> dict:
        """
        Loads the 'tests' object from the JSON for the given test_id.
        Returns the full tests dict so callers can access ["data"]["payload"] etc.
        """
        target_id = test_id if test_id else getattr(self, '_current_test_id', None)
        app_name = getattr(self, 'app_name', 'demo')
        env = os.getenv("ENV") or getattr(self, 'profile', 'qa')
        app_path = f"applications/api/{app_name}"

        try:
            raw = JSONLoader.load_environment_data(app_path, env, target_id)
            if raw:
                return raw.get("tests", raw)   # return the tests block; fall back to raw if key absent
            return {}
        except Exception as e:
            self.logger.warning(f"Could not resolve API test data for {target_id}: {e}")
            return {}

