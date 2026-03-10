import pytest
import os
from core.ui.common.driver_manager import DriverManager
from core.ui.common.singleton import SingletonMeta
from core.ui.common.base_app import BaseApp
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager
from core.utils.json_loader import JSONLoader
from core.utils.video_recorder import VideoRecorder
from applications.web.demo.app.demo_app import DemoApp

class BaseTest(BaseApp):
    """
    Foundational base class for all automated test cases.

    Inherits from `BaseApp` to provide direct access to the shared driver 
    and configuration. It manages the test lifecycle via pytest fixtures 
    and provides utilities for data-driven testing using JSON loaders.

    Attributes:
        app (DemoApp): The application orchestrator for the current project.
        recorder (VideoRecorder): The local screen recorder.
    """
    app: DemoApp = None
    recorder: VideoRecorder = None
    
    def get_test_data(self, filename: str) -> dict:
        """
        Loads raw JSON test data for the current application context.

        Args:
            filename (str): The name of the JSON file (without extension).

        Returns:
            dict: The parsed JSON content.
        """
        app_path = 'applications/web/demo' # Dynamic path resolution can be added later
        return JSONLoader.load_test_data(app_path, filename)

    def get_data_for_test(self, test_id: str = None) -> dict:
        """
        Retrieves a specifically mapped data object for a Test Case ID.

        Prioritizes data cached by the `@test_case` decorator if used. 
        Otherwise, it loads the data dynamically based on the provided ID.

        Args:
            test_id (str, optional): The target Test Case ID (e.g., 'CT-001').

        Returns:
            dict: The key-value data mappings for the test.

        Raises:
            ValueError: If no valid test context or ID is identified.
        """
        # If no ID provided, try to use the one from decorator cache
        target_id = test_id if test_id else getattr(self, '_current_test_id', None)
        
        # If we have the data already in cache for this ID, return it
        if hasattr(self, '_current_test_data') and getattr(self, '_current_test_id', None) == target_id:
            return self._current_test_data
            
        if not target_id:
            raise ValueError("No Test ID provided and no @test decorator found for context.")
            
        content = self.get_test_data(target_id)
        return JSONLoader.get_test_case_data(content)

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """
        Automated Setup and Teardown fixture for individual test cases.
        Resolves configuration defaults from decorators or environment variables.
        """
        # Clear Singleton instances
        SingletonMeta.clear_instances()

        # 1. Resolve Application and Profile
        app_name = getattr(self, 'app_name', 'demo')
        app_type = getattr(self, 'app_type', 'web')
        app_path = f"applications/{app_type}/{app_name}"
        
        # 2. Resolve Environment (Priority: ENV Var > Decorator > Default 'qa')
        env_default = getattr(self, 'profile', 'qa')
        env = os.getenv("ENV", env_default)
        
        # Load configuration
        ConfigManager.load_config(app_path, env)
        
        # 3. Resolve Browser (Priority: BROWSER Var > Decorator > Config > 'chrome')
        browser_default = getattr(self, 'browser', ConfigManager.get("default.browser", "chrome"))
        browser = os.getenv("BROWSER", browser_default)
        
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        
        # --- ROBUST LOG HEADER ---
        # Look for metadata attached by @test_case decorator
        func = request.node.function
        test_id = getattr(func, '_test_id', 'N/A')
        test_title = getattr(func, '_test_title', request.node.name)
        
        # Combine test title, context, and name into a single log string so the UI rendering logic
        # visually groups them inside the same .log-header CSS block.
        header_text = f"🚀 STARTING TEST: {test_id} - {func.__name__}\nTest: {test_title}\nContext: App={app_name} | Env={env} | Browser={browser} (Headless: {headless})"
        self.logger.info(header_text)
        
        try:
            # Initialize and configure the driver instance
            driver_instance = DriverManager.get_driver(browser, headless)
            
            try:
                # Firefox can sometimes throw 'Browsing context has been discarded' on immediate maximize
                driver_instance.maximize_window()
            except Exception as e:
                self.logger.warning(f"Could not maximize window (likely Firefox quirk): {e}")
            
            # Set global driver context
            BaseApp.set_driver(driver_instance)
            
            # Initialize App Orchestrator
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
        # Provide a clean reference to the video URL for the front-end before finalizing
        if hasattr(self, 'recorder') and self.recorder and getattr(self.recorder, 'video_path', None):
            self.logger.info(f"🎥 Video URL: {self.recorder.video_path}")
            
        self.logger.info(f"🏁 FINISHED TEST: {test_id}")


        self.logger.info("Closing WebDriver session")
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            BaseApp.set_driver(None)
