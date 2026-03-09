from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class AlertActions(BaseAction):
    """
    Specialized component for handling JavaScript browser dialogs.
    
    Provides methods to interact with Alerts, Confirms, and Prompts,
    including accepting, dismissing, and sending text input.
    """
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def wait_presence(self, timeout: int = 10):
        """
        Explicitly waits for an alert to be present.
        
        Args:
            timeout (int): Maximum time to wait.
            
        Returns:
            AlertActions: The current instance for method chaining.
        """
        self.at(timeout)._get_wait().until(EC.alert_is_present())
        return self

    @allure.step("Accepting browser alert")
    def accept(self):
        """
        Accepts the current alert (Clicks OK).
        """
        try:
            alert = self.driver.switch_to.alert
            self.logger.info(f"Accepting alert with text: {alert.text}")
            alert.accept()
            return self
        except Exception as e:
            self._handle_exception(e, "accept")

    @allure.step("Dismissing browser alert")
    def dismiss(self):
        """
        Dismisses the current alert (Clicks Cancel).
        """
        try:
            alert = self.driver.switch_to.alert
            self.logger.info(f"Dismissing alert with text: {alert.text}")
            alert.dismiss()
            return self
        except Exception as e:
            self._handle_exception(e, "dismiss")

    def get_text(self) -> str:
        """
        Retrieves the text message displayed in the alert.
        
        Returns:
            str: The alert message.
        """
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            self.logger.info(f"Retrieved alert text: {text}")
            return text
        except Exception as e:
            self._handle_exception(e, "get_text")

    @allure.step("Typing '{text}' into prompt")
    def type(self, text: str):
        """
        Sends text input to a JavaScript prompt.
        
        Args:
            text (str): The text to enter.
            
        Returns:
            AlertActions: The current instance for method chaining.
        """
        try:
            alert = self.driver.switch_to.alert
            self.logger.info(f"Sending text to prompt: {text}")
            alert.send_keys(text)
            return self
        except Exception as e:
            self._handle_exception(e, "type")
