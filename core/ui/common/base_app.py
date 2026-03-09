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
