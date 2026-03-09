import os
import shutil
from core.utils.logger_config import setup_logger

class Cleaner:
    """
    Utility for cleaning up test artifacts like reports and videos.
    """
    logger = setup_logger("Cleaner")

    @staticmethod
    def clean_reports(path: str = "reports"):
        """
        Deletes all files and subdirectories within the specified reports directory.
        
        Args:
            path (str): The path to the reports directory. Defaults to 'reports'.
        """
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            return

        Cleaner.logger.info(f"Cleaning reports directory: {abs_path}")
        
        try:
            # We don't delete the root directory itself, just its contents
            for filename in os.listdir(abs_path):
                file_path = os.path.join(abs_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    Cleaner.logger.error(f"Failed to delete {file_path}. Reason: {e}")
            
            Cleaner.logger.info("Reports directory cleaned successfully.")
        except Exception as e:
            Cleaner.logger.error(f"Error while cleaning reports: {e}")
