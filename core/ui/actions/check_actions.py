from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class CheckActions(BaseAction):
    """
    Specialized actions for interacting with Checkboxes.

    This component provides high-level methods to ensure a checkbox reaches 
    a specific toggle state, handling the current state check automatically.
    """
    @allure.step("Setting checkbox state to {state}")
    def check(self, state: bool = True):
        """
        Sets the checkbox to the desired state.

        Args:
            state (bool): True to check, False to uncheck.

        Returns:
            CheckActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            current_state = self.is_checked()
            if current_state != state:
                self.logger.info(f"Toggling checkbox {self._locator} to {state}")
                self._element.click()
            return self
        except Exception as e:
            self._handle_exception(e, "check")

    @allure.step("Checking selection state")
    def is_checked(self) -> bool:
        """
        Checks if the element is currently selected/checked.
        
        Returns:
            bool: True if the element is selected, False otherwise.
        """
        try:
            self._find_element()
            return self._element.is_selected()
        except Exception as e:
            self._handle_exception(e, "is_checked")
