from selenium.webdriver.remote.webdriver import WebDriver
from core.ui.actions.base_action import BaseAction
from selenium.webdriver.support import expected_conditions as EC
import allure

class ScrollActions(BaseAction):
    """
    Component for handling page and element scrolling interactions.

    Provides methods for scrolling to specific elements, the top of the page, 
    or the absolute bottom of the document using JavaScript execution.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the ScrollActions component.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)

    @allure.step("Scrolling to element with offset {pixels}")
    def to_element(self, pixels: int = 0):
        """
        Scrolls the page until the specified element is centered in the viewport.

        Uses 'scrollIntoView' with 'block: center' to minimize interference from 
        sticky headers/footers, followed by an optional pixel offset.

        Args:
            pixels (int, optional): Additional vertical offset in pixels. 
                Positive values scroll further down. Defaults to 0.

        Returns:
            ScrollActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            
            # 1. Use scrollIntoView with 'center' to avoid fixed headers
            self.driver.execute_script("""
                arguments[0].scrollIntoView({
                    behavior: 'auto',
                    block: 'center'
                });
            """, self._element)

            # 2. Apply optional vertical offset
            if pixels != 0:
                self.driver.execute_script(f"window.scrollBy(0, {pixels});")

            self.logger.info(f"Scrolled to element {self._locator} with offset {pixels}")
            return self
        except Exception as e:
            self._handle_exception(e, "to_element")

    @allure.step("Scrolling element to viewport center")
    def to_center(self):
        """
        Scrolls the specified element to the exact center of the page.

        Calculates the scroll position mathematically using the viewport height 
        and the element's bounding rectangle.

        Returns:
            ScrollActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Scrolling element {self._locator} to center page.")

            js_calculation = """
                var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
                var elementTop = arguments[0].getBoundingClientRect().top;
                window.scrollBy(0, elementTop - (viewPortHeight / 2));
            """
            self.driver.execute_script(js_calculation, self._element)
            return self
        except Exception as e:
            self._handle_exception(e, "to_center")

    @allure.step("Scrolling to bottom of the page")
    def to_bottom(self):
        """
        Scrolls to the absolute bottom of the document via JavaScript.

        Returns:
            ScrollActions: The current instance for method chaining.
        """
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return self
        except Exception as e:
            self._handle_exception(e, "to_bottom")

    @allure.step("Scrolling to top of the page")
    def to_top(self):
        """
        Scrolls to the absolute top of the document via JavaScript.

        Returns:
            ScrollActions: The current instance for method chaining.
        """
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            return self
        except Exception as e:
            self._handle_exception(e, "to_top")
