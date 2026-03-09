from selenium.webdriver.common.by import By
from core.ui.common.base_page import BasePage
import allure

class LoginPage(BasePage):
    """
    Page Object Model representing the SauceDemo Login Page.

    Provides high-level methods to interact with the login form using 
    the fluent interface.

    Locators:
        USERNAME_FIELD (tuple): Locator for the username input.
        PASSWORD_FIELD (tuple): Locator for the password input.
        LOGIN_BUTTON (tuple): Locator for the login submission button.
    """
    # Locators for the login form elements
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    @allure.step("Entering username: {username}")
    def enter_username(self, username: str):
        """
        Enters the username into the username field.

        Args:
            username (str): The username string.

        Returns:
            LoginPage: The current instance for method chaining.
        """
        self.element(self.USERNAME_FIELD).type(username)
        return self

    @allure.step("Entering password")
    def enter_password(self, password: str):
        """
        Enters the password into the password field.

        Args:
            password (str): The password string.

        Returns:
            LoginPage: The current instance for method chaining.
        """
        self.element(self.PASSWORD_FIELD).type(password)
        return self

    @allure.step("Clicking login button")
    def click_login(self):
        """
        Clicks the login button.

        Returns:
            LoginPage: The current instance for method chaining.
        """
        self.element(self.LOGIN_BUTTON).click()
        return self

    def login(self, username=None, password=None):
        """
        Performs a full login sequence by reusing granular methods.
        Uses configuration defaults if arguments are not provided.

        Args:
            username (str, optional): The username to enter.
            password (str, optional): The password to enter.

        Returns:
            LoginPage: The current instance for further verification.
        """
        user = username if username else self.username
        pwd = password if password else self.password
        
        self.logger.info(f"Logging in with user: {user}")
        return self.enter_username(user) \
                   .enter_password(pwd) \
                   .click_login()

    def get_error_message(self) -> str:
        """Retrieves the error message text if present."""
        return self.element(self.ERROR_MESSAGE).wait_visible().get_text()

    def is_login_successful(self) -> bool:
        """
        Confirms if the login was successful by checking the URL.
        
        Returns:
            bool: True if redirected to inventory, False otherwise.
        """
        return "inventory.html" in self.driver.current_url
