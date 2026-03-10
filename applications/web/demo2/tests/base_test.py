import pytest
import os
from core.ui.common.driver_manager import DriverManager
from core.ui.common.singleton import SingletonMeta
from core.ui.common.base_app import BaseApp
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager
from applications.web.demo2.app.demo2_app import Demo2App
from core.utils.video_recorder import VideoRecorder

class Demo2BaseTest(BaseApp):
    app: Demo2App = None
    recorder: VideoRecorder = None
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        SingletonMeta.clear_instances()

        # Resolve Environment & Settings
        app_path = "applications/web/demo2"
        env = os.getenv("ENV", "qa")
        ConfigManager.load_config(app_path, env)
        
        browser = os.getenv("BROWSER", ConfigManager.get("default.browser", "chrome"))
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        
        # Init Driver
        try:
            driver_instance = DriverManager.get_driver(browser, headless)
            driver_instance.maximize_window()
            BaseApp.set_driver(driver_instance)
            self.app = Demo2App()
            
            # Initialize and start video recording
            self.recorder = VideoRecorder(name=request.node.name)
            self.recorder.start()
        except Exception as e:
            raise e
            
        yield
        
        # Stop recording
        if self.recorder:
            self.recorder.stop()
            
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            BaseApp.set_driver(None)
