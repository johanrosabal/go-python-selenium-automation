from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager
from selenium.webdriver.remote.webdriver import WebDriver
import logging

class BaseApp:
    """
    Foundational base class for the entire automation framework.

    Provides a centralized access point for the WebDriver instance, logger, 
    and global configuration. This class facilitates state sharing between 
    tests, Page Objects, and action components.

    Attributes:
        _driver (WebDriver, optional): The class-level shared WebDriver instance.
    """
    _driver = None

    @classmethod
    def set_driver(cls, driver: WebDriver):
        """
        Assigns the global WebDriver instance to the class.

        Args:
            driver (WebDriver): The active Selenium WebDriver instance.
        """
        cls._driver = driver

    @property
    def driver(self) -> WebDriver:
        """
        Retrieves the currently active class-level WebDriver instance.

        Returns:
            WebDriver: The shared Selenium driver.
        """
        return self._driver

    @property
    def config(self) -> ConfigManager:
        """
        Provides direct access to the ConfigManager class for YAML settings.

        Returns:
            ConfigManager: The configuration management utility.
        """
        return ConfigManager

    @property
    def base_url(self) -> str:
        """
        Retrieves the base URL from the currently loaded configuration.

        Returns:
            str: The target environment's base URL.
        """
        return self.config.get("web.base_url")

    @property
    def username(self) -> str:
        """
        Retrieves the default username from the active configuration.

        Returns:
            str: The login username.
        """
        return self.config.get("user.username")

    @property
    def password(self) -> str:
        """
        Retrieves the default password from the active configuration.

        Returns:
            str: The login password.
        """
        return self.config.get("user.password")

    @property
    def logger(self) -> logging.Logger:
        """
        Retrieves a component-specific logger instance.

        The logger is automatically named after the implementing class 
        name (e.g., 'LoginPage').

        Returns:
            logging.Logger: The configured logger for this component.
        """
        if not hasattr(self, "_logger"):
            self._logger = setup_logger(self.__class__.__name__)
        return self._logger
    def get_current_url(self) -> str:
        """
        Retrieves the current browser URL.

        Returns:
            str: The current URL.
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """
        Retrieves the current page title.

        Returns:
            str: The page title.
        """
        return self.driver.title

    def pause(self, seconds: int = 1):
        """
        Pauses execution for a specified duration.

        Args:
            seconds (int): Number of seconds to wait. Defaults to 1.
        """
        import time
        self.logger.info(f"Pausing for {seconds} second(s)...")
        time.sleep(seconds)
        return self

    def screenshot(self, name: str = "Screenshot", full_page: bool = True):
        """
        Takes a screenshot of the current browser state and attaches it to the Allure report.

        Args:
            name (str): The name to display in the Allure report for this screenshot.
            full_page (bool): If True, captures the entire page height. Defaults to True.
        """
        if self._driver:
            import allure
            try:
                self.logger.info(f"Capturing screenshot: {name} (Full Page: {full_page})")
                
                if full_page:
                    # Attempt CDP (Chrome DevTools Protocol) for robust full-page capture if available (Chrome/Edge)
                    if hasattr(self._driver, "execute_cdp_cmd"):
                        import base64
                        # 1. Get total dimensions via JS
                        width = self._driver.execute_script("return Math.max(document.body.parentNode.scrollWidth, document.body.scrollWidth, document.documentElement.scrollWidth, document.documentElement.clientWidth);")
                        height = self._driver.execute_script("return Math.max(document.body.parentNode.scrollHeight, document.body.scrollHeight, document.documentElement.scrollHeight, document.documentElement.clientHeight);")
                        
                        # 2. Set virtual device metrics to encompass the whole page
                        self._driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                            "mobile": False,
                            "width": width,
                            "height": height,
                            "deviceScaleFactor": 1,
                            "fitWindow": False
                        })
                        
                        # 3. Capture screenshot via CDP
                        res = self._driver.execute_cdp_cmd("Page.captureScreenshot", {
                            "format": "png",
                            "fromSurface": True,
                            "captureBeyondViewport": True
                        })
                        
                        # 4. Reset device metrics to return to normal
                        self._driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})
                        png_bytes = base64.b64decode(res['data'])
                    else:
                        # Fallback for non-chromium browsers (Firefox/Safari)
                        original_size = self._driver.get_window_size()
                        width = self._driver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth);")
                        height = self._driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
                        self._driver.set_window_size(width, height)
                        png_bytes = self._driver.get_screenshot_as_png()
                        self._driver.set_window_size(original_size['width'], original_size['height'])
                else:
                    png_bytes = self._driver.get_screenshot_as_png()

                allure.attach(
                    png_bytes,
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                self.logger.error(f"Failed to capture screenshot '{name}': {e}")
        else:
            self.logger.warning("WebDriver is not initialized. Cannot take screenshot.")
