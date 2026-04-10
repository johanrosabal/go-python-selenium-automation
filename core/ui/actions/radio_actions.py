from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class RadioActions(BaseAction):
    """
    Specialized actions for interacting with Radio Buttons.

    This component provides high-level methods to ensure a radio button 
    is selected, handling the current state check automatically.
    """
    @allure.step("Selecting radio button")
    def select_radio(self):
        """
        Selects the radio button if not already selected.

        Returns:
            RadioActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            if not self.is_selected():
                self.logger.info(f"Selecting radio button: {self._locator}")
                self._element.click()
            return self
        except Exception as e:
            self._handle_exception(e, "select_radio")

    def is_selected(self) -> bool:
        """
        Checks if the radio button is currently selected.
            
        Returns:
            bool: True if selected, False otherwise.
        """
        try:
            self._find_element()
            return self._element.is_selected()
        except Exception as e:
            self._handle_exception(e, "is_selected")
