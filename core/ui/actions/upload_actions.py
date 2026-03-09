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
    def file(self, file_path: str):
        """
        Uploads a file to the input element.

        If the provided file_path does not exist, it attempts to find it 
        within the 'resources/uploads' directory.
        
        Args:
            file_path (str): Relative path, absolute path, or just the filename.

        Returns:
            UploadActions: The current instance for method chaining.
        """
        try:
            target_path = file_path
            
            # 1. Resolve path: Check absolute, then relative, then in resources/uploads
            if not os.path.isabs(target_path) and not os.path.exists(target_path):
                # Attempt to find it in the project root's resources/uploads
                project_root = os.getcwd()
                default_dir = os.path.join(project_root, "resources", "uploads")
                potential_path = os.path.join(default_dir, file_path)
                
                if os.path.exists(potential_path):
                    target_path = potential_path
                    self.logger.info(f"Resolved file '{file_path}' to: {target_path}")

            if not os.path.exists(target_path):
                self.logger.error(f"File not found in direct path or resources/uploads: {file_path}")
                raise FileNotFoundError(f"File not found: {file_path}")
                
            abs_path = os.path.abspath(target_path)
            self._find_element()
            self._element.send_keys(abs_path)
            return self
        except Exception as e:
            self._handle_exception(e, "file")
