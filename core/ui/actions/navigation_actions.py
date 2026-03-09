from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class NavigationActions(BaseAction):
    """
    Specialized component for browser-level navigation.

    Includes methods for URL redirection, history traversal (back/forward), 
    page refreshing, and URL-based synchronization.
    """

    def go(self, base_url: str, url: str):
        """
        Navigates to a concatenated URL and waits for the page to load completely.

        Args:
            base_url (str): The base domain or path.
            url (str): The relative path to append.

        Returns:
            NavigationActions: The current instance for method chaining.
        """
        try:
            full_url = str(base_url).rstrip('/') + '/' + str(url).lstrip('/')
            self.logger.debug(f"Go to: {full_url}")
            self.driver.get(full_url)
            self._get_wait().until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return self
        except Exception as e:
            self._handle_exception(e, "go", (base_url, url))

    @allure.step("Navigating to URL: {url}")
    def to_url(self, url: str):
        """
        Alias for go_to_url to support BasePage.open().
        """
        return self.go_to_url(url)

    def go_to_url(self, url: str):
        """
        Directly navigates to the provided URL. Alias for to_url with explicit logging.

        Args:
            url (str): The target URL.

        Returns:
            NavigationActions: The current instance for method chaining.
        """
        try:
            self.logger.debug(f"Go to: {url}")
            self.driver.get(url)
            return self
        except Exception as e:
            self._handle_exception(e, "go_to_url")

    def get_current_url(self) -> str:
        """
        Retrieves the URL of the currently active browser page.

        Returns:
            str: The current URL string.
        """
        try:
            url = self.driver.current_url
            self.logger.info(f"Current URL: [{url}]")
            return url
        except Exception as e:
            self._handle_exception(e, "get_current_url")

    def back(self):
        """
        Navigates one step back in the browser's history.

        Returns:
            NavigationActions: The current instance for method chaining.
        """
        self.driver.back()
        return self

    def forward(self):
        """
        Navigates one step forward in the browser's history.

        Returns:
            NavigationActions: The current instance for method chaining.
        """
        self.driver.forward()
        return self

    def refresh(self):
        """
        Refreshes the current page.

        Returns:
            NavigationActions: The current instance for method chaining.
        """
        self.driver.refresh()
        return self

    def wait_url_contains(self, partial_url: str):
        """
        Waits until the current browser URL contains the specified text.

        Args:
            partial_url (str): The snippet of text to look for in the URL.

        Returns:
            NavigationActions: The current instance for method chaining.

        Raises:
            TimeoutException: If the URL does not contain the text within timeout.
        """
        try:
            self._get_wait().until(EC.url_contains(partial_url))
            return self
        except Exception as e:
            self._handle_exception(e, "wait_url_contains")
