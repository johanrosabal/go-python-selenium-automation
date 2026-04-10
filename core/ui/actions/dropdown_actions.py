from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from core.ui.actions.base_action import BaseAction
import allure

class DropdownActions(BaseAction):
    """
    Component for interacting with selection elements like standard HTML dropdowns.

    Utilizes the Selenium 'Select' support class to provide robust interaction 
    with <select> and <option> tags.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the DropdownActions component.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)

    @allure.step("Selecting option '{text}' from dropdown")
    def select_by_text(self, text: str):
        """
        Selects an option by its exact visible text.

        Args:
            text (str): The visible text of the option.

        Returns:
            DropdownActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Selecting option '{text}' from dropdown {self._locator}")
            select = Select(self._element)
            select.select_by_visible_text(text)
            return self
        except Exception as e:
            self._handle_exception(e, "select_by_text")

    @allure.step("Selecting value '{value}' from dropdown")
    def select_by_value(self, value: str):
        """
        Selects an option by its 'value' attribute.

        Args:
            value (str): The value attribute of the option.

        Returns:
            DropdownActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Selecting value '{value}' from dropdown {self._locator}")
            select = Select(self._element)
            select.select_by_value(value)
            return self
        except Exception as e:
            self._handle_exception(e, "select_by_value")

    @allure.step("Selecting index {index} from dropdown")
    def select_by_index(self, index: int):
        """
        Selects an option by its index.

        Args:
            index (int): The zero-based index.

        Returns:
            DropdownActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Selecting index {index} from dropdown {self._locator}")
            select = Select(self._element)
            select.select_by_index(index)
            return self
        except Exception as e:
            self._handle_exception(e, "select_by_index")

    @allure.step("Selecting option containing text '{text}' from dropdown")
    def select_by_partial_text(self, text: str):
        """
        Selects an option that contains the specified partial text.

        Args:
            text (str): The partial visible text.

        Returns:
            DropdownActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Selecting option containing '{text}' from dropdown {self._locator}")
            select = Select(self._element)
            for option in select.options:
                if text in option.text:
                    select.select_by_visible_text(option.text)
                    break
            return self
        except Exception as e:
            self._handle_exception(e, "select_by_partial_text")

    @allure.step("Deselecting all options from dropdown")
    def deselect_all(self):
        """
        Deselects all options (only works for multi-select dropdowns).

        Returns:
            DropdownActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            self.logger.info(f"Deselecting all options from dropdown {self._locator}")
            select = Select(self._element)
            if select.is_multiple:
                select.deselect_all()
            else:
                self.logger.warning(f"Dropdown {self._locator} is not multi-select. Cannot deselect all.")
            return self
        except Exception as e:
            self._handle_exception(e, "deselect_all")

    @allure.step("Getting all options from dropdown")
    def get_dropdown_options(self) -> list[str]:
        """
        Retrieves the visible text of all options within the dropdown.

        Returns:
            list[str]: A list of option texts.
        """
        try:
            self._find_element()
            self.logger.info(f"Retrieving all options from dropdown {self._locator}")
            select = Select(self._element)
            return [option.text for option in select.options]
        except Exception as e:
            self._handle_exception(e, "get_dropdown_options")
