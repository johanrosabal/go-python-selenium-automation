from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from core.ui.actions.base_action import BaseAction
from selenium.common.exceptions import TimeoutException
import allure

class ElementsActions(BaseAction):
    """
    Component for handling general element-related operations and state checks.

    Provides high-level methods to verify visibility, presence, enabled state, 
    and other properties of UI elements. Also handles generic page-level 
    synchronization.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the ElementsActions component.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)

    @allure.step("Getting element")
    def get_element(self) -> WebElement:
        """
        Waits for and returns the WebElement based on the set locator.

        Returns:
            WebElement: The found web element.
        """
        try:
            return self._find_element()
        except Exception as e:
            self._handle_exception(e, "get_element")

    @allure.step("Checking if element is visible")
    def is_visible(self) -> bool:
        """
        Checks if the element is currently visible on the page.

        Returns:
            bool: True if visible, False otherwise.
        """
        try:
            self._get_wait().until(EC.visibility_of_element_located(self._locator))
            return True
        except:
            return False

    @allure.step("Checking if element is not visible")
    def is_not_visible(self) -> bool:
        """
        Checks if the element is either not present or not visible.

        Returns:
            bool: True if invisible/absent, False otherwise.
        """
        try:
            self._get_wait().until(EC.invisibility_of_element_located(self._locator))
            return True
        except:
            return False

    @allure.step("Checking if element is present in DOM")
    def is_present(self) -> bool:
        """
        Checks if the element is present in the DOM, regardless of visibility.

        Returns:
            bool: True if exists in the DOM, False otherwise.
        """
        try:
            self._get_wait().until(EC.presence_of_element_located(self._locator))
            return True
        except:
            return False

    @allure.step("Checking if element is enabled")
    def is_enabled(self) -> bool:
        """
        Checks if the element is currently enabled.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.get_element().is_enabled()

    @allure.step("Checking if element is selected")
    def is_selected(self) -> bool:
        """
        Checks if the element (checkbox, radio, option) is selected.

        Returns:
            bool: True if selected, False otherwise.
        """
        return self.get_element().is_selected()

    @allure.step("Getting CSS property {property_name} from element")
    def get_css_value(self, property_name: str) -> str:
        """
        Retrieves the value of a specific CSS property for the element.

        Args:
            property_name (str): The CSS property name (e.g., 'color').

        Returns:
            str: The CSS property value.
        """
        return self.get_element().value_of_css_property(property_name)

    @allure.step("Waiting for text '{text}' to be present in element")
    def wait_for_text(self, text: str) -> bool:
        """
        Waits until the specified text is present in the element.

        Args:
            text (str): The text string to wait for.

        Returns:
            bool: True if the text appeared within timeout, False otherwise.
        """
        try:
            self._get_wait().until(EC.text_to_be_present_in_element(self._locator, text))
            return True
        except:
            return False

    @allure.step("Checking if element is clickable")
    def is_clickable(self) -> bool:
        """
        Checks if the element is currently clickable (visible and enabled).

        Returns:
            bool: True if clickable, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(self._locator))
            return True
        except:
            return False

    @allure.step("Waiting for element to be clickable")
    def wait_clickable(self) -> bool:
        """
        Waits until the element is clickable.

        Returns:
            bool: True if the element became clickable.
        """
        try:
            self._get_wait().until(EC.element_to_be_clickable(self._locator))
            return True
        except Exception as e:
            self._handle_exception(e, "wait_clickable")

    @allure.step("Setting CSS property {property_name} to '{value}'")
    def set_css_value(self, property_name: str, value: str):
        """
        Sets a CSS property for the element via direct JavaScript execution.

        Args:
            property_name (str): The CSS property name.
            value (str): The value to set.

        Returns:
            ElementsActions: Self for method chaining.
        """
        element = self.get_element()
        self.driver.execute_script(f"arguments[0].style.{property_name} = '{value}';", element)
        return self

    @allure.step("Waiting for page to load completely")
    def wait_for_page_load(self, timeout: int = 30):
        """
        Waits until the document state is 'complete' via JavaScript.

        Args:
            timeout (int): Maximum time to wait in seconds. Defaults to 30.

        Returns:
            ElementsActions: The current instance for method chaining.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.logger.error("Timeout waiting for page load")
        return self

    @allure.step("Waiting for JavaScript events/async tasks to complete")
    def wait_for_js_completion(self, timeout: int = 20):
        """
        Waits for generic asynchronous JavaScript or jQuery activity to complete.

        Args:
            timeout (int): Maximum time to wait in seconds. Defaults to 20.

        Returns:
            ElementsActions: The current instance for method chaining.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return (window.jQuery != None) ? (jQuery.active == 0) : true")
            )
        except TimeoutException:
            self.logger.warning("Timeout waiting for JS completion (jQuery active or slow async)")
        return self

    @allure.step("Waiting for element to disappear")
    def wait_disappear(self, timeout: int = None):
        """
        Wait until the element explicitly disappears from the viewport or DOM.

        Args:
            timeout (int, optional): Custom timeout for this wait.

        Returns:
            ElementsActions: The current instance for method chaining.
        """
        wait = self.at(timeout)._get_wait() if timeout else self._get_wait()
        try:
            wait.until(EC.invisibility_of_element_located(self._locator))
            self.logger.info(f"Element {self._locator} has disappeared.")
            return self
        except Exception as e:
            self._handle_exception(e, "wait_disappear")

    @allure.step("Checking if element {locator} is enabled via JavaScript")
    def is_enabled_js(self, locator: tuple) -> bool:
        """
        Checks if an element is enabled using direct JavaScript execution.

        Args:
            locator (tuple): The (By, Value) locator of the element.

        Returns:
            bool: True if enabled, False otherwise.
        """
        element = self.get_element(locator)
        return not self.driver.execute_script("return arguments[0].disabled;", element)
