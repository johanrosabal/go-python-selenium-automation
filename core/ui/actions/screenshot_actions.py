import os
from datetime import datetime
import allure
from core.ui.actions.base_action import BaseAction

class ScreenshotActions(BaseAction):
    """
    Specialized component for capturing and managing screenshots.
    
    Provides methods for full-page and element-level screenshots, with 
    automatic integration with Allure reports and local file saving.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.last_filepath = None
    def capture(self, name: str = "screenshot"):
        """
        Captures a screenshot of the current browser viewport.

        The screenshot is automatically attached to the Allure report and 
        saved locally in the 'screenshots' directory.

        Args:
            name (str, optional): A descriptive name for the screenshot. 
                Defaults to "screenshot".

        Returns:
            ScreenshotActions: The current instance for method chaining.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            
            # Ensure screenshots directory exists
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            filepath = os.path.join(screenshot_dir, filename)
            
            # Save locally
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Viewport screenshot saved to: {filepath}")
            
            # Attach to Allure
            allure.attach.file(
                filepath, 
                name=name, 
                attachment_type=allure.attachment_type.PNG
            )
            
            self.last_filepath = filepath
            return self
        except Exception as e:
            self._handle_exception(e, "capture")

    def full_page(self, name: str = "full_page_screenshot"):
        """
        Captures a screenshot of the entire scrollable page height.

        Utilizes Chromium DevTools Protocol (CDP) for Chrome/Edge or 
        native Selenium 4 full-page capture for Firefox.

        Args:
            name (str, optional): Descriptive name. Defaults to "full_page_screenshot".

        Returns:
            ScreenshotActions: The current instance for method chaining.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            
            screenshot_dir = os.path.join("screenshots", "full_page")
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            filepath = os.path.join(screenshot_dir, filename)
            browser_name = self.driver.capabilities.get('browserName', '').lower()

            if browser_name in ['chrome', 'msedge']:
                # Use CDP to capture beyond viewport
                import base64
                res = self.driver.execute_cdp_cmd('Page.captureScreenshot', {
                    'fromSurface': True,
                    'captureBeyondViewport': True
                })
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(res['data']))
            elif browser_name == 'firefox':
                # Use native Firefox full-page capture
                self.driver.get_full_page_screenshot_as_file(filepath)
            else:
                # Fallback to standard viewport screenshot for other browsers
                self.driver.save_screenshot(filepath)
                self.logger.warning(f"Full-page screenshot not natively supported for {browser_name}. Captured viewport instead.")

            self.logger.info(f"Full-page screenshot saved to: {filepath}")
            
            # Attach to Allure
            allure.attach.file(
                filepath, 
                name=name, 
                attachment_type=allure.attachment_type.PNG
            )
            
            self.last_filepath = filepath
            return self
        except Exception as e:
            self._handle_exception(e, "full_page")

    def screenshot(self, name: str = "element_screenshot"):
        """
        Captures a screenshot of the specified UI element.

        Args:
            name (str, optional): Descriptive name. Defaults to "element_screenshot".

        Returns:
            ScreenshotActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            
            # Ensure screenshots directory exists
            screenshot_dir = os.path.join("screenshots", "elements")
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            filepath = os.path.join(screenshot_dir, filename)
            
            # Capture element screenshot
            self._element.screenshot(filepath)
            self.logger.info(f"Element screenshot saved to: {filepath}")
            
            # Attach to Allure
            allure.attach.file(
                filepath, 
                name=name, 
                attachment_type=allure.attachment_type.PNG
            )
            
            self.last_filepath = filepath
            return self
        except Exception as e:
            self._handle_exception(e, "screenshot")
