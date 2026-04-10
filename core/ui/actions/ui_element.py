from typing import Union, List, Dict
from selenium.webdriver.remote.webdriver import WebDriver
from core.ui.actions.base_action import BaseAction
from core.ui.actions.click_actions import ClickActions
from core.ui.actions.send_keys_actions import SendKeysActions
from core.ui.actions.scroll_actions import ScrollActions
from core.ui.actions.dropdown_actions import DropdownActions
from core.ui.actions.elements_actions import ElementsActions
from core.ui.actions.check_actions import CheckActions
from core.ui.actions.radio_actions import RadioActions
from core.ui.actions.table_actions import TableActions
from core.ui.actions.upload_actions import UploadActions
from core.ui.actions.get_text_actions import GetTextActions
from core.ui.actions.screenshot_actions import ScreenshotActions
import allure

class UIElement(BaseAction):
    """
    Primary interface for interacting with UI elements (Facade Pattern).

    This class binds a Selenium locator to a comprehensive set of actions 
    (Click, SendKeys, Select, etc.), providing a fluent and intuitive API.
    It handles automatic logging with Page Object context and dynamic 
    timeout management.
    """
    def __init__(self, driver: WebDriver, locator: tuple, page_object=None):
        """
        Initializes the UIElement facade.

        Args:
            driver (WebDriver): The active Selenium WebDriver instance.
            locator (tuple): The (By, Value) locator for this element.
            page_object (BasePage, optional): The parent Page Object for context.
        """
        super().__init__(driver)
        self.locator = locator
        self.page_object = page_object
        
        # Metadata discovery for logging
        self.page_name = page_object.__class__.__name__ if page_object else "UnknownPage"
        self.locator_name = self._discover_locator_name()
        
        # Initialize internal action components
        self._click = ClickActions(self.driver).set_locator(self.locator)
        self._send_keys = SendKeysActions(self.driver).set_locator(self.locator)
        self._scroll = ScrollActions(self.driver).set_locator(self.locator)
        self._select = DropdownActions(self.driver).set_locator(self.locator)
        self._elements = ElementsActions(self.driver).set_locator(self.locator)
        self._check = CheckActions(self.driver).set_locator(self.locator)
        self._radio = RadioActions(self.driver).set_locator(self.locator)
        self._table = TableActions(self.driver).set_locator(self.locator)
        self._upload = UploadActions(self.driver).set_locator(self.locator)
        self._get_text = GetTextActions(self.driver).set_locator(self.locator)
        self._screenshot = ScreenshotActions(self.driver).set_locator(self.locator)

    def _discover_locator_name(self) -> str:
        """
        Performs a reverse lookup to find the variable name of the locator.

        Uses the parent Page Object's class dictionary to identify how 
        this locator was named in the code (e.g., 'LOGIN_BUTTON').

        Returns:
            str: The name of the locator or its value if not found.
        """
        if not self.page_object:
            return str(self.locator)
        
        for name, value in self.page_object.__class__.__dict__.items():
            if value == self.locator:
                return name
        return str(self.locator)

    def _log_action(self, action: str):
        """
        Logs a UI action with metadata context.

        Args:
            action (str): Description of the action being performed.
        """
        self.logger.info(f"{self.page_name} - {action} on element: {self.locator_name} {self.locator}")

    # --- Click Actions ---

    def click(self):
        """
        Performs a standard click on the element.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Clicking")
        self._click.at(self._get_current_timeout()).element()
        return self

    def double_click(self):
        """
        Performs a double-click on the element.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Double clicking")
        self._click.at(self._get_current_timeout()).double_click()
        return self

    def right_click(self):
        """
        Performs a right-click on the element.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Right clicking")
        self._click.at(self._get_current_timeout()).right_click()
        return self

    def hover(self):
        """
        Moves the mouse pointer over the element.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Moving mouse to")
        self._click.at(self._get_current_timeout()).move_to_element()
        return self

    def js_click(self):
        """
        Clicks the element using JavaScript.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Clicking via JS")
        self._click.at(self._get_current_timeout()).js_click()
        return self

    def click_and_hold(self):
        """
        Clicks and holds the element.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Clicking and holding")
        self._click.at(self._get_current_timeout()).click_and_hold()
        return self

    def release_mouse(self):
        """
        Releases the mouse button.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Releasing mouse")
        self._click.at(self._get_current_timeout()).release()
        return self

    def release(self):
        """
        Alias for release_mouse().
        """
        return self.release_mouse()

    def drag_and_drop(self, target_locator: tuple):
        """
        Drags this element and drops it onto a target locator.

        Args:
            target_locator (tuple): The (By, Value) of the destination.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Dragging to {target_locator}")
        self._click.at(self._get_current_timeout()).drag_and_drop(target_locator)
        return self

    # --- SendKeys Actions ---

    def type(self, text: str, clear: bool = True):
        """
        Enters text into the element (input/textarea).

        Args:
            text (str): The string to type.
            clear (bool, optional): Whether to clear the field first. Defaults to True.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Typing '{text}' into")
        self._send_keys.at(self._get_current_timeout()).set_text(text, clear=clear)
        return self

    def type_encrypted(self, text: str, clear: bool = True):
        """
        Enters text and masks it in logs using base64.

        Args:
            text (str): The sensitive string to type.
            clear (bool, optional): Whether to clear the field first. Defaults to True.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Typing encrypted text into")
        self._send_keys.at(self._get_current_timeout()).encrypted().set_text(text, clear=clear)
        return self

    def type_js(self, text: str, clear: bool = False):
        """
        Sets element value via JavaScript (bypasses some event blockers).

        Args:
            text (str): The text to set.
            clear (bool): Whether to clear first.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Setting text '{text}' via JS in")
        self._send_keys.at(self._get_current_timeout()).set_text_js(text, clear=clear)
        return self

    def type_by_character(self, text: str):
        """
        Simulates human typing by sending one character at a time.

        Args:
            text (str): The text to type.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Typing '{text}' character by character into")
        self._send_keys.at(self._get_current_timeout()).set_text_by_character(text)
        return self

    def clear(self, use_js: bool = False):
        """
        Clears the input field.

        Args:
            use_js (bool, optional): Whether to use JS events for clearing. Defaults to False.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Clearing")
        self._send_keys.at(self._get_current_timeout()).clear(use_js=use_js)
        return self

    def physical_clear(self):
        """
        Clears the input using keyboard shortcuts (CTRL+A + BACKSPACE).

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Performing physical clear")
        self._send_keys.at(self._get_current_timeout()).physical_clear()
        return self

    def press(self, key: str):
        """
        Sends a specific keyboard key stroke to the element.

        Args:
            key (str): The key to press (e.g., Keys.ENTER).

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Pressing key '{key}' on")
        self._send_keys.at(self._get_current_timeout()).press_key(key)
        return self

    def press_enter(self):
        """
        Presses the ENTER key.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Pressing ENTER on")
        self._send_keys.at(self._get_current_timeout()).press_enter()
        return self

    def press_tab(self):
        """
        Presses the TAB key.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Pressing TAB on")
        self._send_keys.at(self._get_current_timeout()).press_tab()
        return self

    def press_escape(self):
        """
        Presses the ESCAPE key.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Pressing ESCAPE on")
        self._send_keys.at(self._get_current_timeout()).press_escape()
        return self

    def press_backspace(self):
        """
        Presses the BACKSPACE key.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Pressing BACKSPACE on")
        self._send_keys.at(self._get_current_timeout()).press_backspace()
        return self

    def press_return(self):
        """
        Presses the RETURN key.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Pressing RETURN on")
        self._send_keys.at(self._get_current_timeout()).press_return()
        return self

    # --- Scroll Actions ---

    def scroll_to(self, pixels: int = 0):
        """
        Scrolls the page until this element is centered in the viewport.

        Args:
            pixels (int, optional): Additional vertical offset. Defaults to 0.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Scrolling to (offset: {pixels})")
        self._scroll.at(self._get_current_timeout()).to_element(pixels)
        return self

    def scroll_to_center(self):
        """
        Scrolls the element to the exact center of the page.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Scrolling to exact center")
        self._scroll.at(self._get_current_timeout()).to_center()
        return self

    def scroll_to_top(self):
        """
        Scrolls to the absolute top of the page.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Scrolling to top of page")
        self._scroll.at(self._get_current_timeout()).to_top()
        return self

    def scroll_to_bottom(self):
        """
        Scrolls to the absolute bottom of the page.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Scrolling to bottom of page")
        self._scroll.at(self._get_current_timeout()).to_bottom()
        return self

    # --- Select Actions ---

    def select_by_text(self, text: str):
        """
        Selects an option from a dropdown element by visible text.

        Args:
            text (str): The text of the option to select.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Selecting '{text}' from dropdown")
        self._select.at(self._get_current_timeout()).text(text)
        return self

    def select_by_partial_text(self, text: str):
        """
        Selects an option containing the specified partial text.

        Args:
            text (str): Partial text to look for.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Selecting option containing '{text}' from dropdown")
        self._select.at(self._get_current_timeout()).partial_text(text)
        return self

    def select_by_value(self, value: str):
        """
        Selects an option by its value attribute.

        Args:
            value (str): The value to select.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Selecting value '{value}' from dropdown")
        self._select.at(self._get_current_timeout()).value(value)
        return self

    def select_by_index(self, index: int):
        """
        Selects an option by its zero-based index.

        Args:
            index (int): The index to select.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Selecting index {index} from dropdown")
        self._select.at(self._get_current_timeout()).index(index)
        return self

    def deselect_all(self):
        """
        Deselects all options from a multi-select dropdown.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Deselecting all from")
        self._select.at(self._get_current_timeout()).deselect_all()
    def get_dropdown_options(self) -> list[str]:
        """
        Retrieves all available options from a dropdown element.

        Returns:
            list[str]: List of option texts.
        """
        return self._select.at(self._get_current_timeout()).get_options()

    def check(self, state: bool = True):
        """
        Ensures a checkbox reaches the specified toggle state.

        Args:
            state (bool): True to check, False to uncheck. Defaults to True.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Setting checkbox state to {state} for")
        self._check.at(self._get_current_timeout()).set_state(state)
        return self

    def is_checked(self) -> bool:
        """
        Returns the current selection state of a checkbox.

        Returns:
            bool: True if selected, False otherwise.
        """
        return self._check.at(self._get_current_timeout()).is_checked()

    # --- Radio Actions ---

    def select_radio(self):
        """
        Ensures the radio button is selected.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Selecting radio button")
        self._radio.at(self._get_current_timeout()).select()
        return self

    def is_selected(self) -> bool:
        """
        Returns the current selection state of a radio button.

        Returns:
            bool: True if selected, False otherwise.
        """
        return self._radio.at(self._get_current_timeout()).is_selected()

    # --- Table Actions ---

    def get_cell_text(self, row: int, col: Union[int, str]) -> str:
        """
        Retrieves text from a specific cell if this element is a table.

        Args:
            row (int): 1-based row index.
            col (Union[int, str]): 1-based column index or name.

        Returns:
            str: The cell content.
        """
        self._log_action(f"Getting text from cell ({row}, {col}) of")
        return self._table.at(self._get_current_timeout()).get_cell_text(row, col)

    def get_row_count(self) -> int:
        """
        Returns the total number of rows in the table.

        Returns:
            int: The row count.
        """
        return self._table.at(self._get_current_timeout()).get_row_count()

    def get_table_headers(self) -> list[str]:
        """
        Retrieves all header texts from a table.

        Returns:
            list[str]: Header titles.
        """
        return self._table.at(self._get_current_timeout()).get_headers()

    def click_table_header(self, text: str = None, index: int = None):
        """
        Clicks a table header for sorting or selection.

        Args:
            text (str, optional): Header text.
            index (int, optional): 1-based index.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(self._get_current_timeout()).click_header(text, index)
        return self

    def get_table_data(self) -> list[dict]:
        """
        Extracts the entire table content into a structured list of dictionaries.

        Returns:
            list[dict]: Table data.
        """
        return self._table.at(self._get_current_timeout()).get_all_data()

    def table_check_all(self, column: Union[int, str] = 1):
        """
        Clicks the global selection checkbox in the table.

        Args:
            column (Union[int, str], optional): The 1-based column identifier. Defaults to 1.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(self._get_current_timeout()).check_all(column)
        return self

    def table_check_row(self, index: int, column: Union[int, str] = 1):
        """
        Clicks the selection checkbox for a specific row and column.

        Args:
            index (int): 1-based row index.
            column (Union[int, str], optional): The 1-based column identifier. Defaults to 1.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(self._get_current_timeout()).check_row(index, column)
        return self

    def table_click_button(self, row: int, col: Union[int, str], text: str = None):
        """
        Clicks a button within a specific table cell.

        Args:
            row (int): 1-based row index.
            col (Union[int, str]): 1-based column identifier.
            text (str, optional): Filter text for the button.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(self._get_current_timeout()).click_button_in_cell(row, col, text)
        return self

    def table_click_link(self, row: int, col: Union[int, str], text: str = None):
        """
        Clicks a link within a specific table cell.

        Args:
            row (int): 1-based row index.
            col (Union[int, str]): 1-based column identifier.
            text (str, optional): Filter text for the link.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(self._get_current_timeout()).click_link_in_cell(row, col, text)
        return self

    def table_wait_for_rows(self, expected_count: int, timeout: int = None):
        """
        Waits until the table has a specific number of rows.

        Args:
            expected_count (int): Row count to wait for.
            timeout (int, optional): Custom timeout.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(timeout if timeout else self._get_current_timeout()).wait_for_rows(expected_count)
        return self

    def table_wait_not_empty(self, timeout: int = None):
        """
        Waits until the table is no longer empty.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._table.at(timeout if timeout else self._get_current_timeout()).wait_not_empty()
        return self

    # --- Upload Actions ---

    def upload_file(self, file_path: str):
        """
        Uploads a file using this element as the file input.

        Args:
            file_path (str): Path to the file.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Uploading file '{file_path}' to")
        self._upload.at(self._get_current_timeout()).file(file_path)
        return self

    # --- Elements/State Actions ---

    def wait_visible(self):
        """
        Explicitly waits for the element to become visible.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Waiting for visibility of")
        self._elements.at(self._get_current_timeout()).is_visible()
        return self

    def wait_present(self):
        """
        Explicitly waits for the element to be present in the DOM.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Waiting for presence of")
        self._elements.at(self._get_current_timeout()).is_present()
        return self

    def wait_clickable(self):
        """
        Explicitly waits for the element to be clickable (visible and enabled).

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Waiting for element to be clickable")
        self._elements.at(self._get_current_timeout()).wait_clickable()
        return self

    def wait_disappear(self, timeout: int = None):
        """
        Explicitly waits for the element to disappear from the viewport or DOM.

        Args:
            timeout (int, optional): Custom timeout for this wait.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action("Waiting for disappearance of")
        self._elements.at(timeout if timeout else self._get_current_timeout()).wait_disappear()
        return self

    def is_enabled(self) -> bool:
        """
        Checks if the element is currently enabled.

        Returns:
            bool: True if enabled.
        """
        return self._elements.at(self._get_current_timeout()).is_enabled()

    def is_clickable(self) -> bool:
        """
        Checks if the element is currently clickable.

        Returns:
            bool: True if clickable.
        """
        return self._elements.at(self._get_current_timeout()).is_clickable()

    def is_enabled_js(self) -> bool:
        """
        Checks if the element is enabled using direct JavaScript execution.

        Returns:
            bool: True if enabled via JS.
        """
        return self._elements.at(self._get_current_timeout()).is_enabled_js()

    def get_css_value(self, property_name: str) -> str:
        """
        Retrieves a CSS property value.

        Args:
            property_name (str): The property name.

        Returns:
            str: The property value.
        """
        return self._elements.at(self._get_current_timeout()).get_css_value(property_name)

    def set_css_value(self, property_name: str, value: str):
        """
        Sets a CSS property via JS.

        Args:
            property_name (str): Property name.
            value (str): Value to set.

        Returns:
            UIElement: Self for chaining.
        """
        self._log_action(f"Setting CSS {property_name}={value} on")
        self._elements.at(self._get_current_timeout()).set_css_value(property_name, value)
        return self

    def is_not_visible(self) -> bool:
        """
        Checks if the element is not visible or not present.

        Returns:
            bool: True if not visible.
        """
        return self._elements.at(self._get_current_timeout()).is_not_visible()

    def get_text(self) -> str:
        """
        Retrieves the visible text of the element.

        Returns:
            str: The element text.
        """
        # self._log_action("Getting text from") # Removed log for getter to reduce noise
        return self._get_text.at(self._get_current_timeout()).text()

    def get_trimmed_text(self) -> str:
        """
        Retrieves the element text with whitespace removed.

        Returns:
            str: The cleaned text.
        """
        return self._get_text.at(self._get_current_timeout()).trimmed()

    def get_attribute(self, attribute: str) -> str:
        """
        Retrieves the value of a specific attribute.

        Args:
            attribute (str): Attribute name.

        Returns:
            str: Attribute value.
        """
        return self._get_text.at(self._get_current_timeout()).attribute(attribute)

    def get_value(self) -> str:
        """
        Direct access to the 'value' attribute (common for inputs).

        Returns:
            str: The input value.
        """
        return self._get_text.at(self._get_current_timeout()).value()

    def wait_text_contains(self, text: str):
        """
        Waits until the element text contains a partial string.

        Args:
            text (str): Partial text to wait for.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Waiting for text '{text}' in")
        self._elements.at(self._get_current_timeout()).wait_for_text(text)
        return self

    def contains_text(self, text: str) -> bool:
        """
        Checks if the element text currently contains a partial string.

        Args:
            text (str): Partial text to look for.

        Returns:
            bool: True if found.
        """
        return self._get_text.at(self._get_current_timeout()).contains(text)

    def wait_until_text_is(self, text: str):
        """
        Waits until the element text matches exactly the expected string.

        Args:
            text (str): Exact text.

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Waiting until text is exactly '{text}' in")
        self._get_text.at(self._get_current_timeout()).wait_until_is(text)
        return self

    def matches_regex(self, pattern: str) -> bool:
        """
        Validates the element text against a regular expression.

        Args:
            pattern (str): The regex pattern.

        Returns:
            bool: True if matches.
        """
        return self._get_text.at(self._get_current_timeout()).matches_regex(pattern)

    def is_empty(self) -> bool:
        """
        Checks if the element has no text content.

        Returns:
            bool: True if empty.
        """
        return self._get_text.at(self._get_current_timeout()).is_empty()

    # --- HTML / Technical Retrieval ---

    def get_inner_html(self) -> str:
        """
        Retrieves the internal HTML content of the element.

        Returns:
            str: Inner HTML code.
        """
        return self._get_text.at(self._get_current_timeout()).inner_html()

    def get_outer_html(self) -> str:
        """
        Retrieves the full HTML code including the element's own tags.

        Returns:
            str: Outer HTML code.
        """
        return self._get_text.at(self._get_current_timeout()).outer_html()

    def get_text_content(self) -> str:
        """
        Captures all text content via DOM 'textContent' (includes hidden text).

        Returns:
            str: Full text content.
        """
        return self._get_text.at(self._get_current_timeout()).text_content()

    # --- Numeric Parsing ---

    def get_int(self) -> int:
        """
        Parses the element text and returns the first integer found.

        Returns:
            int: The parsed number.
        """
        return self._get_text.at(self._get_current_timeout()).get_int()

    def get_float(self) -> float:
        """
        Parses the element text and returns the first decimal found.

        Returns:
            float: The parsed float.
        """
        return self._get_text.at(self._get_current_timeout()).get_float()

    # --- Multi-Element Retrieval ---

    def all_texts(self) -> list[str]:
        """
        Retrieves a list of texts for all items matching the element's locator.

        Returns:
            list[str]: Collection of text strings.
        """
        return self._get_text.at(self._get_current_timeout()).all_texts()

    # --- Screenshot Actions ---

    def screenshot(self, name: str = "element_screenshot"):
        """
        Captures a screenshot of this specific element.

        Args:
            name (str, optional): Descriptive name. Defaults to "element_screenshot".

        Returns:
            UIElement: Self instance for method chaining.
        """
        self._log_action(f"Taking screenshot '{name}' of")
        self._screenshot.at(self._get_current_timeout()).element(name)
        return self

    def is_visible(self) -> bool:
        """
        Immediate check for element visibility.

        Returns:
            bool: True if visible.
        """
        return self._elements.at(self._get_current_timeout()).is_visible()

    # --- Helper logic ---

    def _get_current_timeout(self) -> int:
        """
        Internal helper to extract the active fluent timeout for delegation.

        Returns:
            int: Current timeout in seconds.
        """
        return int(self._current_wait._timeout)
