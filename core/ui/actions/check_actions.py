from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class CheckActions(BaseAction):
    """
    Specialized actions for interacting with Checkboxes.

    This component provides high-level methods to ensure a checkbox reaches 
    a specific toggle state, handling the current state check automatically.
    """
    @allure.step("Setting checkbox/radio state to {state}")
    def set_state(self, state: bool):
        """
        Sets the checkbox or radio button to the desired state.

        If the element is already in the target state, no action is taken.
        Otherwise, a click is performed to toggle it.
        
        Args:
            state (bool): True to ensure it is checked/selected, False for unchecked.

        Returns:
            CheckActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            is_selected = self._element.is_selected()
            
            if is_selected != state:
                self._element.click()
                self.logger.info(f"Checkbox state changed to {state}")
            else:
                self.logger.info(f"Checkbox already in state {state}")
            return self
        except Exception as e:
            self._handle_exception(e, "set_state")

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
