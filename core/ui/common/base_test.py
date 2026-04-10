import pytest
import os
from core.ui.common.driver_manager import DriverManager
from core.ui.common.singleton import SingletonMeta
from core.ui.common.base_app import BaseApp
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager
from core.utils.json_loader import JSONLoader
from core.utils.video_recorder import VideoRecorder

class BaseTest(BaseApp):
    """
    Foundational base class for all automated test cases.

    Inherits from `BaseApp` to provide direct access to the shared driver 
    and configuration. It manages the test lifecycle via pytest fixtures 
    and provides utilities for data-driven testing using JSON loaders.

    Attributes:
        persistent_session (bool): If True, the browser session is maintained 
                                   across all test methods in the class.
        app (BaseApp): The application orchestrator for the current project.
        recorder (VideoRecorder): The local screen recorder.
    """
    persistent_session: bool = False
    _shared_driver = None
    
    app: BaseApp = None
    recorder: VideoRecorder = None
    
    @pytest.fixture(scope="class", autouse=True)
    def _class_driver_cleanup(self):
        """Internal fixture to ensure context-level driver cleanup."""
        yield
        if BaseTest._shared_driver:
            from core.ui.common.base_app import BaseApp
            BaseTest._shared_driver.quit()
            BaseTest._shared_driver = None
            BaseApp.set_driver(None)

    def get_test_data(self, test_id: str = None) -> dict:
        # ... (unchanged) ...
        target_id = test_id if test_id else getattr(self, '_current_test_id', None)
        
        # 1. Yield pre-loaded data if it accurately matches the requested ID
        if hasattr(self, '_current_test_data') and getattr(self, '_current_test_id', None) == target_id:
            if self._current_test_data:
                return self._current_test_data
                
        if not target_id:
            raise ValueError("No Test ID provided and no @test_case decorator found for context.")
            
        # 2. Perform live resolution if cache missed (e.g., loading an external json)
        app_name = getattr(self, 'app_name', 'demo')
        app_type = getattr(self, 'app_type', 'web')
        
        env = os.getenv("ENV")
        if not env:
            env = getattr(self, 'profile', 'qa')
            
        app_path = f"applications/{app_type}/{app_name}"
        
        try:
            from core.utils.json_loader import JSONLoader
            # Attempt Environmental Data Load directly
            env_content = JSONLoader.load_environment_data(app_path, env, target_id)
            if env_content:
                return JSONLoader.get_test_case_data(env_content)
                
            # Fallback to standard data location
            content = JSONLoader.load_test_data(app_path, target_id)
            return JSONLoader.get_test_case_data(content)
        except Exception as e:
            self.logger.warning(f"Could not dynamically resolve test data for {target_id}: {e}")
            return {}

    def get_data_for_test(self, test_id: str = None) -> dict:
        """Alias for get_test_data() to maintain backwards compatibility."""
        return self.get_test_data(test_id)

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """
        Automated Setup and Teardown fixture for individual test cases.
        Resolves configuration defaults from decorators or environment variables.
        """
        # Clear Singleton instances (except the driver if persistent)
        SingletonMeta.clear_instances()

        # 1. Resolve Application and Profile
        app_name = getattr(self, 'app_name', 'demo')
        app_type = getattr(self, 'app_type', 'web')
        app_path = f"applications/{app_type}/{app_name}"
        
        # 2. Resolve Environment (Priority: ENV Var > Decorator > Default 'qa')
        env = os.getenv("ENV")
        if not env:
            env = getattr(self, 'profile', 'qa')
        
        # Load configuration
        ConfigManager.load_config(app_path, env)
        
        # 3. Resolve Browser (Priority: BROWSER Var > Decorator > Config > 'chrome')
        browser = os.getenv("BROWSER")
        if not browser:
            browser = getattr(self, 'browser', ConfigManager.get("default.browser", "chrome"))
        
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        
        # --- ROBUST LOG HEADER & DYNAMIC JSON METADATA ---
        func = request.node.function
        test_id = getattr(func, '_test_id', 'N/A')
        json_file_fallback = getattr(func, '_test_json_file', None)
        
        # 4. Load JSON Metadata dynamically here because we finally have Context (App & Env)
        self._current_test_id = test_id
        self._current_test_data = {}
        
        # Priority Fallbacks explicitly provided via `@test_case` arguments
        arg_title = getattr(func, '_test_arg_title', None)
        arg_desc = getattr(func, '_test_arg_description', None)
        
        try:
            from core.utils.json_loader import JSONLoader
            
            # 1. Try Environment-Specific JSON matching the test ID
            env_content = JSONLoader.load_environment_data(app_path, env, test_id)
            
            # 2. Try Generic Fallback JSON if env_content is empty
            if not env_content and json_file_fallback:
                env_content = JSONLoader.load_test_data(app_path, json_file_fallback)
                
            if env_content:
                metadata = env_content.get("tests", {})
                self._current_test_data = metadata.get("data", {})
                func._test_metadata = metadata  # Crucial for wrapper to consume Allure tags
                
                # Resolving properties using Priority Queue: JSON -> Args -> Default
                func._test_title = metadata.get("title") or arg_title or func.__name__
                func._test_description = metadata.get("description") or arg_desc or "No description provided."
        except Exception:
            pass

        test_title = getattr(func, '_test_title', arg_title or request.node.name)
        test_desc = getattr(func, '_test_description', arg_desc or "No description provided.")
        self._current_test_title = test_title
        
        # Combine test title, context, and name into a single log string so the UI rendering logic
        # visually groups them inside the same .log-header CSS block.
        header_text = f"🚀 STARTING TEST: {test_id} - {test_title}\nDescription: {test_desc}\nMethod: {func.__name__}\nContext: App={app_name} | Env={env} | Browser={browser} (Headless: {headless})"
        self.logger.info(header_text)
        
        try:
            # --- WEBDRIVER ACQUISITION STRATEGY ---
            if self.persistent_session and BaseTest._shared_driver:
                driver_instance = BaseTest._shared_driver
                self.logger.info("♻️ Reusing persistent browser session for this test.")
            else:
                # Initialize new driver instance
                driver_instance = DriverManager.get_driver(browser, headless)
                
                try:
                    driver_instance.maximize_window()
                except Exception as e:
                    self.logger.warning(f"Could not maximize window: {e}")
                
                if self.persistent_session:
                    BaseTest._shared_driver = driver_instance
                    self.logger.info("📡 Persistent session enabled. Driver will be shared across the class.")
            
            # Set global driver context
            BaseApp.set_driver(driver_instance)
            
            # Initialize App Orchestrator dynamically based on the app context
            if app_name == 'go_hotel':
                from applications.web.go_hotel.app.go_hotel_app import GoHotelApp
                self.app = GoHotelApp()
            else:
                from applications.web.demo.app.demo_app import DemoApp
                self.app = DemoApp()

            # Initialize and start video recording
            self.recorder = VideoRecorder(name=request.node.name)
            self.recorder.start()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise e
        
        yield
        
        # Cleanup routine
        if self.recorder:
            self.recorder.stop()

        # --- ROBUST LOG FOOTER ---
        if hasattr(self, 'recorder') and self.recorder and getattr(self.recorder, 'video_path', None):
            self.logger.info(f"🎥 Video URL: {self.recorder.video_path}")
            
        self.logger.info(f"🏁 FINISHED TEST: {test_id}")

        # --- TERMINATION STRATEGY ---
        if not self.persistent_session:
            self.logger.info("Closing WebDriver session (Isolation mode)")
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                BaseApp.set_driver(None)
        else:
            self.logger.info("Keeping WebDriver session alive (Persistence mode)")
