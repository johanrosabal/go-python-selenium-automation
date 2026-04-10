from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class ClickActions(BaseAction):
    """
    Component for handling all click and mouse-based interactions.

    Provides a comprehensive set of methods for interacting with elements via 
    mouse actions, including standard clicks, double-clicks, right-clicks, 
    hovering, and drag-and-drop operations.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the ClickActions component.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)

    @allure.step("Clicking on element")
    def single_click(self):
        """
        Performs a standard click on an element.

        Waits for the element to be clickable before performing the action.

        Returns:
            ClickActions: The current instance for method chaining.

        Raises:
            TimeoutException: If the element is not clickable within the timeout.
        """
        try:
            from selenium.webdriver.support import expected_conditions as EC
            element = self._find_element(EC.element_to_be_clickable(self._locator))
            element.click()
            return self
        except Exception as e:
            self._handle_exception(e, "element")

    @allure.step("Double clicking on element")
    def double_click(self):
        """
        Performs a double-click on an element using ActionChains.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        try:
            from selenium.webdriver.support import expected_conditions as EC
            element = self._get_wait().until(EC.element_to_be_clickable(self._locator))
            ActionChains(self.driver).double_click(element).perform()
            return self
        except Exception as e:
            self._handle_exception(e, "double_click")

    @allure.step("Right clicking on element")
    def right_click(self):
        """
        Performs a right-click (context click) on an element using ActionChains.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        try:
            from selenium.webdriver.support import expected_conditions as EC
            element = self._get_wait().until(EC.element_to_be_clickable(self._locator))
            ActionChains(self.driver).context_click(element).perform()
            return self
        except Exception as e:
            self._handle_exception(e, "right_click")

    @allure.step("Clicking on element")
    def click(self):
        """
        Performs a standard click on an element.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Clicking on element: {self._locator}")
            self._element.click()
            return self
        except Exception as e:
            self._handle_exception(e, "click")

    @allure.step("Moving mouse pointer to element")
    def hover(self):
        """
        Moves the mouse pointer over the center of an element.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        try:
            self._find_element()
            self.logger.info(f"Moving mouse pointer to: {self._locator}")
            actions = ActionChains(self.driver)
            actions.move_to_element(self._element).perform()
            return self
        except Exception as e:
            self._handle_exception(e, "hover")

    @allure.step("Clicking and holding on element")
    def click_and_hold(self):
        """
        Clicks and holds the left mouse button on an element.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        try:
            from selenium.webdriver.support import expected_conditions as EC
            element = self._get_wait().until(EC.element_to_be_clickable(self._locator))
            ActionChains(self.driver).click_and_hold(element).perform()
            return self
        except Exception as e:
            self._handle_exception(e, "click_and_hold")

    @allure.step("Releasing mouse button")
    def release_mouse(self):
        """
        Releases the held mouse button over an element.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        try:
            self._find_element()
            self.logger.info(f"Releasing mouse button over: {self._locator}")
            actions = ActionChains(self.driver)
            actions.release(self._element).perform()
            return self
        except Exception as e:
            self._handle_exception(e, "release_mouse")

    @allure.step("Dragging element to target")
    def drag_and_drop(self, target_locator: tuple):
        """
        Performs a full drag and drop operation onto a destination element.

        Args:
            target_locator (tuple): The (By, Value) locator of the destination element.

        Returns:
            ClickActions: The current instance for method chaining.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support import expected_conditions as EC
        try:
            wait = self._get_wait()
            source = self._find_element()
            target = wait.until(EC.visibility_of_element_located(target_locator))
            ActionChains(self.driver).drag_and_drop(source, target).perform()
            return self
        except Exception as e:
            self._handle_exception(e, "drag_and_drop")
