from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction

class RadioActions(BaseAction):
    """
    Specialized actions for interacting with Radio Buttons.

    This component provides high-level methods to ensure a radio button 
    is selected, handling the current state check automatically.
    """
    def select(self):
        """
        Selects the radio button if it is not already selected.

        Returns:
            RadioActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            if not self._element.is_selected():
                self._element.click()
            return self
        except Exception as e:
            self._handle_exception(e, "select")

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
