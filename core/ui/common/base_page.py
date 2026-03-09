from core.ui.common.base_app import BaseApp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.click_actions import ClickActions
from core.ui.actions.send_keys_actions import SendKeysActions
from core.ui.actions.scroll_actions import ScrollActions
from core.ui.actions.dropdown_actions import DropdownActions
from core.ui.actions.elements_actions import ElementsActions
from core.ui.actions.navigation_actions import NavigationActions
from core.ui.actions.switch_windows_actions import SwitchWindowsActions
from core.ui.actions.frame_actions import FrameActions
from core.ui.actions.radio_actions import RadioActions
from core.ui.actions.screenshot_actions import ScreenshotActions
from core.ui.actions.alert_actions import AlertActions
from core.ui.actions.ui_element import UIElement
from core.ui.common.singleton import SingletonMeta
from selenium.webdriver.remote.webdriver import WebDriver

# Advanced Utilities
from core.utils.visual_comparer import VisualComparer
from core.utils.accessibility_tester import AccessibilityTester
from core.utils.performance_monitor import PerformanceMonitor

class BasePage(BaseApp, metaclass=SingletonMeta):
    """
    Foundational Base class for all Page Objects within the framework.

    Inherits from `BaseApp` and implements the `SingletonMeta` pattern to 
    ensure efficient instance reuse across tests. It serves as a central 
    aggregator for specialized action components, providing a fluent and 
    unified interface for UI automation.

    Attributes:
        click (ClickActions): Handler for all mouse-related interactions.
        send_keys (SendKeysActions): Handler for keyboard and text input.
        scroll (ScrollActions): Handler for viewport and element scrolling.
        select (DropdownActions): Handler for standard HTML dropdowns.
        elements (ElementsActions): Handler for element state checks (visibility, etc.).
        navigation (NavigationActions): Handler for browser-level navigation.
        window (SwitchWindowsActions): Handler for window and tab management.
        radio (RadioActions): Handler for radio button interactions.
        screenshot (ScreenshotActions): Handler for screen capture.
        frame (FrameActions): Handler for IFrame context switching.
    """
    def __init__(self, driver: WebDriver = None):
        """
        Initializes the Page Object and its delegated action components.
        
        Args:
            driver (WebDriver, optional): The Selenium WebDriver instance. 
                Defaults to the global driver managed by BaseApp.
        """
        # Default wait time configuration (internal usage)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Action Component Initialization
        self.click = ClickActions(self.driver)
        self.send_keys = SendKeysActions(self.driver)
        self.scroll = ScrollActions(self.driver)
        self.select = DropdownActions(self.driver)
        self.elements = ElementsActions(self.driver)
        self.navigation = NavigationActions(self.driver)
        self.window = SwitchWindowsActions(self.driver)
        self.radio = RadioActions(self.driver)
        self.screenshot = ScreenshotActions(self.driver)
        self.frame = FrameActions(self.driver)
        self.alert = AlertActions(self.driver)
        
        # Advanced Integration
        self.visual = VisualComparer()
        self.a11y = AccessibilityTester(self.driver)
        self.performance = PerformanceMonitor(self.driver)

    def open(self, url: str = None):
        """
        Navigates the browser to the specified URL.

        Args:
            url (str, optional): The destination URL. Defaults to `self.base_url`.

        Returns:
            BasePage: The current instance (Self) for method chaining.
        """
        target_url = url if url else self.base_url
        self.logger.info(f"Navigating to URL: {target_url}")
        self.navigation.to_url(target_url)
        return self

    def open_url(self, url: str):
        """
        Explicitly navigates to a provided URL.

        Args:
            url (str): The target URL string.

        Returns:
            BasePage: The current instance (Self) for method chaining.
        """
        self.navigation.go_to_url(url)
        return self

    def get_url(self) -> str:
        """
        Retrieves the current browser URL.

        Returns:
            str: The current URL.
        """
        return self.get_current_url()

    def get_title(self) -> str:
        """
        Retrieves the current page title.

        Returns:
            str: The page title.
        """
        return self.get_page_title()

    def open_relative(self, path: str):
        """
        Navigates to a path relative to the configured `base_url`.

        Args:
            path (str): The relative path (e.g., "/login").

        Returns:
            BasePage: The current instance (Self) for method chaining.
        """
        full_url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return self.open(full_url)

    def scroll_to_top(self):
        """
        Scrolls the browser window to the absolute top.

        Returns:
            BasePage: The current instance for method chaining.
        """
        self.scroll.to_top()
        return self

    def scroll_to_bottom(self):
        """
        Scrolls the browser window to the absolute bottom.

        Returns:
            BasePage: The current instance for method chaining.
        """
        self.scroll.to_bottom()
        return self

    def wait_for_element(self, locator: tuple):
        """
        Explicitly waits for an element to be visible on the page.

        Args:
            locator (tuple): The (By, Value) locator.

        Returns:
            WebElement: The Selenium element once it becomes visible.
        """
        return self.elements.get_element(locator)

    def wait_for_url(self, partial_url: str, timeout: int = 10):
        """
        Waits until the current browser URL contains the expected substring.

        Args:
            partial_url (str): The snippet of text to look for in the URL.
            timeout (int, optional): Maximum time to wait. Defaults to 10.

        Returns:
            BasePage: The current instance (Self) for method chaining.
        """
        self.navigation.at(timeout).wait_url_contains(partial_url)
        return self

    def wait_for_page_load(self, timeout: int = 30):
        """
        Waits until the document state is 'complete'.

        Args:
            timeout (int): Maximum time to wait in seconds. Defaults to 30.

        Returns:
            BasePage: The current instance for method chaining.
        """
        self.elements.wait_for_page_load(timeout)
        return self

    def wait_for_js_completion(self, timeout: int = 20):
        """
        Waits for generic asynchronous JavaScript activity to complete.

        Args:
            timeout (int): Maximum time to wait in seconds. Defaults to 20.

        Returns:
            BasePage: The current instance for method chaining.
        """
        self.elements.wait_for_js_completion(timeout)
        return self

    def element(self, locator: tuple) -> UIElement:
        """
        Creates a `UIElement` facade for fluent interaction with a specific locator.

        This is the recommended way to perform actions on elements contextually 
        within a Page Object.

        Args:
            locator (tuple): The (By, Value) locator of the element.

        Returns:
            UIElement: A facade instance bound to the locator and this page.
        """
        return UIElement(self.driver, locator, page_object=self)

    # --- God Tier Advanced Methods ---

    def assert_visual_match(self, test_name: str, threshold: float = 0.01):
        """
        Performs a visual comparison of the current page against a baseline.
        """
        self.screenshot.full_page(f"temp_visual_{test_name}")
        current_screenshot = self.screenshot.last_filepath
        match = self.visual.compare(current_screenshot, test_name, threshold)
        assert match, f"Visual regression detected for {test_name}. Check reports/visual/diffs/"
        return self

    def assert_no_accessibility_violations(self, impact_level: str = "critical"):
        """
        Scans the page and fails if violations are found.
        """
        self.a11y.assert_no_violations(self.__class__.__name__, impact_level)
        return self

    def capture_performance_metrics(self):
        """
        Extracts and logs browser performance data.
        """
        return self.performance.capture_metrics(self.__class__.__name__)
