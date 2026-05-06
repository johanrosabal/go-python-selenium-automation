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
        The validation only runs if 'visual.enable' is True in the configuration.
        """
        enabled = self.config.get("visual.enable", True)
        
        if not enabled:
            self.logger.warning(f"Visual validation skipped for '{test_name}' (Disabled in config).")
            return self

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

    # --- Navigation Shortcuts ---

    def open(self, url: str = None):
        """
        Navigates to the specified URL or to the base URL from config.
        
        Args:
            url (str, optional): Target URL. If None, uses web.base_url.
            
        Returns:
            BasePage: The current instance for chaining.
        """
        target = url if url else self.base_url
        self.navigation.open(target)
        return self

    def open_relative(self, path: str):
        """
        Navigates to a path relative to the base URL.
        
        Args:
            path (str): Relative path (e.g. "/inventory").
            
        Returns:
            BasePage: The current instance for chaining.
        """
        self.navigation.go(path)
        return self
