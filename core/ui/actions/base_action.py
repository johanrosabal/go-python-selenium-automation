from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from core.utils.logger_config import setup_logger
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import logging
import allure

class BaseAction:
    """
    Foundational base class for all UI action components.

    Provides essential utilities inherited by specialized action classes, 
    including direct access to WebDriver, support for fluent timeout management 
    via explicit waits, and a centralized exception handling mechanism.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the BaseAction component.

        Args:
            driver (WebDriver): The active Selenium WebDriver instance.
        """
        self.driver = driver
        self.default_timeout = 10
        self._wait = WebDriverWait(self.driver, self.default_timeout)
        self._current_wait = self._wait
        self._locator = None
        self._element = None
        self.logger = setup_logger(self.__class__.__name__)

    def at(self, timeout: int):
        """
        Fluently sets a temporary timeout for the immediate next operation.

        This method allows overriding the default timeout for a specific wait 
        without affecting subsequent actions.

        Args:
            timeout (int): The temporary timeout duration in seconds.

        Returns:
            BaseAction: The current instance for method chaining (fluent API).
        """
        self.logger.debug(f"Setting temporary timeout to {timeout}s")
        self._current_wait = WebDriverWait(self.driver, timeout)
        return self

    def set_locator(self, locator: tuple):
        """
        Sets the locator and clears any previously found element.

        Args:
            locator (tuple): The (By, Value) locator.

        Returns:
            BaseAction: The current instance for method chaining.
        """
        self._locator = locator
        self._element = None
        return self

    def _find_element(self, condition=None):
        """
        Internal helper to find and cache the element using the set locator.
        Includes Auto-healing logic if the primary locator fails.
        
        Args:
            condition: Optional Selenium Expected Condition. 
                       Defaults to presence_of_element_located.
        """
        if not self._locator:
            raise ValueError("Locator not set. Call 'set_locator()' first.")
        
        from selenium.webdriver.support import expected_conditions as EC
        cond = condition if condition else EC.presence_of_element_located(self._locator)
        
        try:
            # 1. Primary Attempt
            self._element = self._get_wait().until(cond)
            return self._element
        except (TimeoutException, NoSuchElementException):
            # 2. Auto-healing Attempt
            self.logger.warning(f"[AUTO-HEALING] Primary locator {self._locator} failed. Attempting recovery...")
            healed_element = self._attempt_healing()
            if healed_element:
                self.logger.warning(f"[AUTO-HEALING] Successfully recovered element using fuzzy matching!")
                self._element = healed_element
                return self._element
            raise # Re-raise original if healing fails

    def _attempt_healing(self):
        """
        Tries to find the element using alternative strategies.
        Phase 1: Fuzzy matching by text or partial attributes.
        """
        by, value = self._locator
        
        # Strategy A: If it's an ID or Name, try 'contains'
        if by in ["id", "name"]:
            selectors = [
                 f"//*[contains(@{by}, '{value}')]",
                 f"//*[@*[contains(., '{value}')]]"
            ]
            for xpath in selectors:
                elements = self.driver.find_elements("xpath", xpath)
                if elements: return elements[0]

        # Strategy B: If it's XPath/CSS, try to find by text if value contains quotes
        # Example: //button[text()='Login'] -> //button[contains(text(), 'Login')]
        if "text()" in value:
             clean_text = value.split("'")[1] if "'" in value else value.split('"')[1] if '"' in value else None
             if clean_text:
                 elements = self.driver.find_elements("xpath", f"//*[contains(text(), '{clean_text}')]")
                 if elements: return elements[0]
        
        return None

    def _get_wait(self) -> WebDriverWait:
        """
        Retrieves the currently active wait object and resets it to default.

        This is an internal helper used by subclasses to ensure that 
        temporary timeouts are only applied once.

        Returns:
            WebDriverWait: The Selenium wait instance to be used for the next action.
        """
        wait = self._current_wait
        self._current_wait = self._wait  # Reset to default
        return wait

    def _handle_exception(self, exception: Exception, method_name: str, locator: tuple = None):
        """
        Centralized logic for exception categorization, logging, and reporting.

        Intercepts common Selenium exceptions to provide descriptive log messages 
        before re-raising them to the test layer.

        Args:
            exception (Exception): The raw exception object.
            method_name (str): The name of the action method where the error originated.
            locator (tuple, optional): The element locator involved in the failure.
                If not provided, uses the internal self._locator.

        Raises:
            Exception: Re-raises the original exception after logging.
        """
        target_locator = locator if locator else self._locator
        msg = f"Error in '{method_name}'"
        if target_locator:
            msg += f" for element {target_locator}"
        
        if isinstance(exception, TimeoutException):
            self.logger.error(f"{msg}: Timeout reached.")
        elif isinstance(exception, NoSuchElementException):
            self.logger.error(f"{msg}: No such element found.")
        elif isinstance(exception, WebDriverException):
            self.logger.error(f"{msg}: WebDriver error -> {getattr(exception, 'msg', str(exception))}")
        else:
            self.logger.error(f"{msg}: Unexpected error -> {str(exception)}")
        
        raise exception
