from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from core.ui.actions.base_action import BaseAction
import allure
from core.utils.base64_utils import encode_base64

class SendKeysActions(BaseAction):
    """
    Component for handling keyboard and text input interactions.

    Provides methods for typing text into input fields, handling field 
    clearing, and sending specific keys (like ENTER, TAB, etc.).
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the SendKeysActions component.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)
        self._encrypt = False

    def encrypted(self):
        """
        Enables base64 encryption for text in logs.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        self._encrypt = True
        return self

    @allure.step("Typing text into element (Clear: {clear})")
    def type(self, text: str, clear: bool = False):
        """
        Sets and sends the provided text to the element.

        Args:
            text (str): The string to type.
            clear (bool): Whether to clear the field first.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        try:
            if not isinstance(text, str):
                raise TypeError("The text argument must be a string.")

            if clear:
                self.clear()

            self._find_element()
            
            log_text = encode_base64(text) if self._encrypt else text
            self.logger.debug(f"Send Keys [{log_text}]")

            self._element.send_keys(text)
            self._encrypt = False
            return self
        except Exception as e:
            self._handle_exception(e, "type")

    @allure.step("Typing text via JavaScript (Clear: {clear})")
    def type_js(self, text: str, clear: bool = False):
        """
        Sets the element value using JavaScript and triggers events.

        Args:
            text (str): The text to set.
            clear (bool): Whether to clear first.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        try:
            if clear:
                self.clear_js()

            self._find_element()
            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, self._element, text)
            return self
        except Exception as e:
            self._handle_exception(e, "type_js")

    @allure.step("Typing text character by character")
    def type_by_character(self, text: str):
        """
        Sends text to the element character by character to simulate human typing.

        Args:
            text (str): The string to type.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        try:
            if not isinstance(text, str):
                raise TypeError("The text argument must be a string.")

            self._find_element()
            log_text = encode_base64(text) if self._encrypt else text
            self.logger.debug(f"Sending text '{log_text}' by character.")

            for letter in text:
                self.logger.debug(f"Sending character: '{letter}'")
                self._element.send_keys(letter)
            
            self._encrypt = False
            return self
        except Exception as e:
            self._handle_exception(e, "type_by_character")

    def get_value(self) -> str:
        """
        Retrieves text from the element's 'value' attribute.

        Returns:
            str: The input value.
        """
        try:
            self._find_element()
            input_value = self._element.get_attribute('value')
            self.logger.debug(f"Retrieved Element Value: {input_value}")
            return input_value
        except Exception as e:
            self._handle_exception(e, "get_value")

    @allure.step("Clearing text (Use JS: {use_js})")
    def clear(self, use_js: bool = False):
        """
        Clears the text from the element.

        Args:
            use_js (bool): Whether to use JavaScript for clearing.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        if use_js:
            return self.clear_js()
            
        try:
            self._find_element()
            self.logger.debug("Clearing text from element.")
            self._element.click()
            self._element.clear()
            return self
        except Exception as e:
            self._handle_exception(e, "clear")

    def clear_js(self):
        """
        Clears input field and triggers necessary JavaScript events.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.driver.execute_script("""
                var element = arguments[0];
                element.value = '';
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new Event('blur', { bubbles: true }));
            """, self._element)
            return self
        except Exception as e:
            self._handle_exception(e, "clear_js")

    @allure.step("Performing physical clear (CONTROL+A + BACKSPACE)")
    def physical_clear(self):
        """
        Simulates physical clearing of an input field using keyboard shortcuts.
        Useful for React/Angular components that don't respond to standard clear().

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        try:
            from selenium.webdriver import Keys
            self._find_element()
            self.logger.debug("Performing physical clear (CTRL+A + BACKSPACE)")
            self._element.send_keys(Keys.CONTROL + "a")
            self._element.send_keys(Keys.BACKSPACE)
            return self
        except Exception as e:
            self._handle_exception(e, "physical_clear")

    def press_enter(self):
        """Presses the ENTER key."""
        return self._press_key(Keys.ENTER, "ENTER")

    def press_tab(self):
        """Presses the TAB key."""
        return self._press_key(Keys.TAB, "TAB")

    def press_escape(self):
        """Presses the ESCAPE key."""
        return self._press_key(Keys.ESCAPE, "ESCAPE")

    def press_backspace(self):
        """Presses the BACKSPACE key."""
        return self._press_key(Keys.BACKSPACE, "BACKSPACE")

    def press_return(self):
        """Presses the RETURN key."""
        return self._press_key(Keys.RETURN, "RETURN")

    @allure.step("Pressing key on element")
    def press(self, key: Keys, key_name: str = "KEY"):
        """
        Sends a keyboard key stroke to the element.

        Args:
            key (Keys): The Selenium Keys constant.
            key_name (str): Label for logging.

        Returns:
            SendKeysActions: The current instance for method chaining.
        """
        return self._press_key(key, key_name)

    def _press_key(self, key, key_name):
        """Internal helper to press a key on the element."""
        try:
            self._find_element()
            self.logger.debug(f"Pressing [{key_name}] key.")
            self._element.send_keys(key)
            return self
        except Exception as e:
            self._handle_exception(e, f"press_{key_name.lower()}")
