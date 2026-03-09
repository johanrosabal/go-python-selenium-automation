from core.ui.actions.base_action import BaseAction
import allure
import time

class SwitchWindowsActions(BaseAction):
    """
    Specialized component for browser window and tab management.

    Handles switching between multiple windows/tabs, closing windows, 
    and maintaining focus on specific browser instances.
    """
    def __init__(self, driver):
        super().__init__(driver)
        # Store the handle of the window that was active during initialization
        self._original_handle = self.driver.current_window_handle if self.driver else None

    def get_current_handle(self) -> str:
        """
        Retrieves the handle of the currently focused window or tab.

        Returns:
            str: The window handle ID.
        """
        if self.driver:
            handle = self.driver.current_window_handle
            self.logger.info(f"Get current window handle: {handle}")
            return handle
        else:
            self.logger.error("Unable to get current window handle. WebDriver is None.")
            return ""

    def get_original_handle(self) -> str:
        """
        Retrieves the handle of the window that was active during action initialization.

        Returns:
            str: The original window handle ID.
        """
        self.logger.info(f"Original window handle: {self._original_handle}")
        return self._original_handle

    @allure.step("Switching to tab index {index}")
    def to_tab(self, index: int):
        """
        Alias for tab().
        """
        return self.tab(index)

    def tab(self, index: int):
        """
        Switches focus to a window or tab by its index in the window handles list.

        Args:
            index (int): The zero-based index of the tab.

        Returns:
            SwitchWindowsActions: The current instance for method chaining.
        """
        if self.driver:
            try:
                handles = self.driver.window_handles
                if 0 <= index < len(handles):
                    self.driver.switch_to.window(handles[index])
                    self.logger.info(f"Switched to tab index {index}")
                    from core.ui.common.base_app import BaseApp
                    BaseApp.pause(1)
                else:
                    self.logger.error(f"Tab index {index} is out of bounds (Total tabs: {len(handles)})")
            except Exception as e:
                self._handle_exception(e, "tab")
        else:
            self.logger.error("Unable to switch tab. WebDriver is None.")
        return self

    @allure.step("Finding and switching to a new window")
    @allure.step("Finding and switching to a new window")
    def switch_to_new(self):
        """
        Alias for find_new().
        """
        return self.find_new()

    def find_new(self):
        """
        Switches focus to the first window handle that is not the 'original' one.
        Useful when an action opens a single new window.

        Returns:
            SwitchWindowsActions: The current instance for method chaining.
        """
        if self.driver:
            try:
                for handle in self.driver.window_handles:
                    if handle != self._original_handle:
                        self.driver.switch_to.window(handle)
                        self.logger.info(f"Switched to new window/tab: {handle}")
                        break
            except Exception as e:
                self._handle_exception(e, "find_new")
        else:
            self.logger.error("Unable to find new window. WebDriver is None.")
        return self

    @allure.step("Opening a new blank tab")
    def open_new(self):
        """
        Opens a new blank tab and automatically switches focus to it.

        Returns:
            SwitchWindowsActions: The current instance for method chaining.
        """
        if self.driver:
            try:
                # Selenium 4 native new window/tab support
                self.driver.switch_to.new_window('tab')
                self.logger.info("Opened and switched to a new blank tab")
            except Exception as e:
                self._handle_exception(e, "open_new")
        else:
            self.logger.error("Unable to open new tab. WebDriver is None.")
        return self

    @allure.step("Closing current tab and returning focus")
    @allure.step("Closing current tab and returning focus")
    def close_current(self):
        """
        Alias for close().
        """
        return self.close()

    def close(self):
        """
        Closes the currently focused window and switches focus back to the original one.

        Returns:
            SwitchWindowsActions: The current instance for method chaining.
        """
        if self.driver:
            try:
                self.logger.info("Closing current window/tab.")
                self.driver.close()
                
                # Switch back to original if it still exists, otherwise to the first available
                handles = self.driver.window_handles
                if self._original_handle in handles:
                    self.driver.switch_to.window(self._original_handle)
                elif len(handles) > 0:
                    self.driver.switch_to.window(handles[0])
            except Exception as e:
                self._handle_exception(e, "close")
        else:
            self.logger.error("Unable to close window. WebDriver is None.")
        return self
    def switch_to_main(self):
        """
        Switches focus to the first window handle (main tab).

        Returns:
            SwitchWindowsActions: The current instance for method chaining.
        """
        return self.tab(0)

    def get_handles(self) -> list:
        """
        Retrieves all active window handles.

        Returns:
            list: List of handles.
        """
        return self.driver.window_handles if self.driver else []
