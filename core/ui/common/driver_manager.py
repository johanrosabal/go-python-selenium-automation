import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
logging.getLogger("WDM").setLevel(logging.WARNING)

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import allure

class DriverManager:
    """
    Factory class to manage WebDriver instances for different browsers.

    This class centralizes the creation and configuration of WebDrivers, 
    supporting Chrome, Firefox, and Edge via webdriver-manager.
    """
    @staticmethod
    def get_driver(browser_name: str = "chrome", headless: bool = False):
        """
        Initializes and returns a WebDriver instance based on the browser name.
        Supports proxy and local driver path from Config.
        """
        from core.utils.config_manager import ConfigManager
        import os

        browser_name = browser_name.lower()
        chrome_path = ConfigManager.get("browser.chrome_path")
        firefox_path = ConfigManager.get("browser.firefox_path")
        edge_path = ConfigManager.get("browser.edge_path")
        proxy_http = ConfigManager.get("proxy.http")
        proxy_https = ConfigManager.get("proxy.https")

        if proxy_http or proxy_https:
            os.environ['HTTP_PROXY'] = proxy_http if proxy_http else ""
            os.environ['HTTPS_PROXY'] = proxy_https if proxy_https else ""
            os.environ['WDM_SSL_VERIFY'] = '0'

        remote_url = ConfigManager.get("remote.url")
        enable_video = ConfigManager.get("remote.enable_video") or False
        enable_vnc = ConfigManager.get("remote.enable_vnc") or False

        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            options.add_argument("--disable-logging")
            
            # Stealth and automation flags
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False
            })

            if headless:
                options.add_argument("--headless")

            if remote_url:
                if enable_video or enable_vnc:
                    options.set_capability("selenoid:options", {
                        "enableVideo": enable_video,
                        "enableVNC": enable_vnc
                    })
                return webdriver.Remote(command_executor=remote_url, options=options)

            try:
                if chrome_path and os.path.exists(chrome_path):
                    service = ChromeService(executable_path=chrome_path)
                else:
                    os.environ['WDM_SSL_VERIFY'] = '0'
                    service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            except Exception as e:
                raise ConnectionError(
                    f"Failed to initialize Chrome driver. Error: {e}. "
                    "Hint: Check your internet connection, proxy settings, or local_path in config."
                )

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            # Stealth and automation flags
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("signon.rememberSignons", False)

            if headless:
                options.add_argument("--headless")

            if remote_url:
                if enable_video or enable_vnc:
                    options.set_capability("selenoid:options", {
                        "enableVideo": enable_video,
                        "enableVNC": enable_vnc
                    })
                return webdriver.Remote(command_executor=remote_url, options=options)

            try:
                if firefox_path and os.path.exists(firefox_path):
                    service = FirefoxService(executable_path=firefox_path)
                else:
                    service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=options)
            except Exception as e:
                raise ConnectionError(
                    f"Failed to initialize Firefox driver. Error: {e}. "
                    "Hint: Check your internet connection, proxy settings, or local_path in config."
                )

        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            options.add_argument("--disable-logging")
            # Stealth and automation flags
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False
            })

            if headless:
                options.add_argument("--headless")

            if remote_url:
                if enable_video or enable_vnc:
                    options.set_capability("selenoid:options", {
                        "enableVideo": enable_video,
                        "enableVNC": enable_vnc
                    })
                return webdriver.Remote(command_executor=remote_url, options=options)

            try:
                if edge_path and os.path.exists(edge_path):
                    service = EdgeService(executable_path=edge_path)
                else:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=options)
            except Exception as e:
                raise ConnectionError(
                    f"Failed to initialize Edge driver. Error: {e}. "
                    "Hint: Check your internet connection, proxy settings, or local_path in config."
                )

        else:
            raise ValueError(f"Browser '{browser_name}' is not supported. Choose from: chrome, firefox, edge.")
