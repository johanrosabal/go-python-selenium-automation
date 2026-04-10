from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure
import re

class GetTextActions(BaseAction):
    """
    Specialized component for retrieving and validating text and values from UI elements.

    Provides a rich set of methods for data extraction, including standard text, 
    trimmed text, attribute values, numeric parsing (int/float), and HTML content.
    Includes built-in support for regex matching and text-based synchronization.
    """
    
    @allure.step("Getting text from element")
    def get_text(self) -> str:
        """
        Retrieves the visible text of the element.

        Returns:
            str: The text content.
        """
        try:
            self._find_element()
            text_value = self._element.text
            self.logger.debug(f"Retrieved text: '{text_value}'")
            return text_value
        except Exception as e:
            self._handle_exception(e, "get_text")

    @allure.step("Getting trimmed text from element")
    def get_trimmed_text(self) -> str:
        """
        Retrieves the element's text and removes leading/trailing whitespace.

        Returns:
            str: The cleaned text content.
        """
        try:
            val = self.get_text()
            return val.strip() if val else ""
        except Exception as e:
            self._handle_exception(e, "get_trimmed_text")

    @allure.step("Getting attribute {attribute} from element")
    def attribute(self, attribute: str) -> str:
        """
        Retrieves the value of a specific attribute from the element.

        Args:
            attribute (str): The name of the attribute (e.g., 'href').

        Returns:
            str: The value of the attribute.
        """
        try:
            self._find_element()
            return self._element.get_attribute(attribute)
        except Exception as e:
            self._handle_exception(e, "attribute")

    @allure.step("Getting value property from element")
    def value(self) -> str:
        """
        Retrieves the 'value' property of an element (common for input fields).

        Returns:
            str: The value of the 'value' attribute/property.
        """
        return self.attribute("value")

    @allure.step("Checking if element contains text '{expected_text}'")
    def contains(self, expected_text: str) -> bool:
        """
        Checks if the element contains the specified partial text.

        Args:
            expected_text (str): The partial text to look for.

        Returns:
            bool: True if found, False otherwise.
        """
        val = self.text()
        return expected_text in val if val else False

    @allure.step("Waiting until element text is exactly '{expected_text}'")
    def wait_until_is(self, expected_text: str):
        """
        Waits until the element text matches the expected text exactly.

        Args:
            expected_text (str): The exact text to wait for.

        Returns:
            GetTextActions: The current instance for method chaining.
        """
        try:
            self._get_wait().until(EC.text_to_be_present_in_element(self._locator, expected_text))
            return self
        except Exception as e:
            self._handle_exception(e, "wait_until_is")

    @allure.step("Checking if element matches regex pattern '{pattern}'")
    def matches_regex(self, pattern: str) -> bool:
        """
        Checks if the element text matches a regular expression pattern.

        Args:
            pattern (str): The regex pattern to validate against.

        Returns:
            bool: True if matches.
        """
        val = self.text()
        return bool(re.match(pattern, val)) if val else False

    @allure.step("Checking if element is empty")
    def is_empty(self) -> bool:
        """
        Returns True if the element text is empty or contains only whitespace.

        Returns:
            bool: True if empty/whitespace.
        """
        val = self.trimmed()
        return not val

    @allure.step("Getting inner HTML of element")
    def inner_html(self) -> str:
        """
        Returns the innerHTML of the element.

        Returns:
            str: The raw inner HTML.
        """
        return self.attribute("innerHTML")

    @allure.step("Getting outer HTML of element")
    def outer_html(self) -> str:
        """
        Returns the outerHTML of the element.

        Returns:
            str: The raw outer HTML.
        """
        return self.attribute("outerHTML")

    @allure.step("Getting textContent of element")
    def text_content(self) -> str:
        """
        Returns the textContent via JavaScript.

        Returns:
            str: The full text content.
        """
        return self.attribute("textContent")

    @allure.step("Extracting integer from element")
    def get_int(self) -> int:
        """
        Extracts the first integer found in the element text.

        Returns:
            int: The extracted integer.
        """
        val = self.text()
        nums = re.findall(r'\d+', val)
        return int(nums[0]) if nums else 0

    @allure.step("Extracting float from element")
    def get_float(self) -> float:
        """
        Extracts the first float found in the element text.

        Returns:
            float: The extracted float.
        """
        val = self.text()
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", val)
        return float(nums[0]) if nums else 0.0

    @allure.step("Getting list of texts from multiple elements")
    def all_texts(self) -> list[str]:
        """
        Returns a list containing the visible text of all elements matching the locator.

        Returns:
            list[str]: A list of strings.
        """
        try:
            elements = self.driver.find_elements(*self._locator)
            return [el.text for el in elements]
        except Exception as e:
            self._handle_exception(e, "all_texts")
