from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class FrameActions(BaseAction):
    """
    Specialized component for Frame and IFrame management.

    Handles switching contexts between the main document and various frames 
    using explicit waits for frame availability.
    """
    def switch_to(self, locator: tuple):
        """
        Switches the driver focus to a specified frame.

        Waits until the frame is available and then automatically switches to it.
        
        Args:
            locator (tuple): The (By, Value) locator of the frame element.

        Returns:
            FrameActions: The current instance for method chaining.

        Raises:
            TimeoutException: If the frame is not available within timeout.
        """
        try:
            self._get_wait().until(EC.frame_to_be_available_and_switch_to_it(locator))
            return self
        except Exception as e:
            self._handle_exception(e, "switch_to_frame", locator)

    def switch_to_parent(self):
        """
        Switches focus to the parent frame of the current frame.

        Returns:
            FrameActions: The current instance for method chaining.
        """
        try:
            self.driver.switch_to.parent_frame()
            return self
        except Exception as e:
            self._handle_exception(e, "switch_to_parent")

    def switch_to_default(self):
        """
        Switches the driver focus back to the main document (default content).

        Returns:
            FrameActions: The current instance for method chaining.
        """
        try:
            self.driver.switch_to.default_content()
            return self
        except Exception as e:
            self._handle_exception(e, "switch_to_default")
