from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import os
import allure

class UploadActions(BaseAction):
    """
    Specialized component for handling file upload interactions.

    Provides a clean interface for interacting with <input type='file'> elements, 
    automatically handling path synchronization.
    """
    
    @allure.step("Uploading file '{file_path}'")
    def upload_file(self, file_path: str):
        """
        Uploads a file by sending its absolute path to the file input element.

        Args:
            file_path (str): The absolute path to the file.

        Returns:
            UploadActions: The current instance for method chaining.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            self._find_element()
            self.logger.info(f"Uploading file to element {self._locator}: {file_path}")
            self._element.send_keys(file_path)
            return self
        except Exception as e:
            self._handle_exception(e, "upload_file")
