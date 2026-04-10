from selenium.webdriver.common.by import By
from core.ui.common.base_page import BasePage
import allure

class LoginPage(BasePage):
    """
    Page Object Model representing the go-hotel Login Page.
    """
    
    RELATIVE = "login"
    # Locators (using data-testid for automation)
    INP_EMAIL = (By.XPATH, "//input[@name='email']")
    INP_PASSWORD = (By.XPATH, "//input[@name='password']")
    BTN_LOGIN = (By.XPATH, "//button[@data-testid='login-submit-button']")

    @allure.step("Waiting for page load")
    def wait_for_page_load(self):
        self.navigation.go(url=self.RELATIVE)
        self.elements.wait_for_page_load()
        self.window.set_zoom_level(75)
        return self

    @allure.step("Entering email: {email}")
    def enter_email(self, email: str):
        self.element(self.INP_EMAIL).clear().type(email)
        return self

    @allure.step("Entering password")
    def enter_password(self, password: str):
        self.element(self.INP_PASSWORD).clear().type(password)
        return self

    @allure.step("Clicking login button")
    def click_login(self):
        self.element(self.BTN_LOGIN).click()
        return self

    @allure.step("Logging in")
    def login(self, email=None, password=None, wait_success=True):
        user_email = email if email else self.username
        user_pwd = password if password else self.password
        
        self.logger.info(f"Logging in with email: {user_email}")
        self.enter_email(user_email).enter_password(user_pwd).click_login()
        
        # Sincronización opcional: Solo esperar si esperamos un éxito
        if wait_success:
            self.navigation.wait_url_contains(partial_url="dashboard")
            
        return self

    def is_login_successful(self) -> bool:
        """
        Checks if the user is already on a dashboard or functional page.
        Returns True if the current URL is valid and does not contain 'login'.
        """
        url = self.navigation.get_current_url()
        # If we are on any functional page, login was successful
        return any(path in url for path in ["dashboard", "reservations", "clients", "order"])

    def is_login_not_logged(self) -> bool:
        """
        Checks if the user needs to log in.
        Returns True if on login page or blank/start pages.
        """
        url = self.navigation.get_current_url()
        if url in ["", "about:blank", "data:,"] or "login" in url:
            return True
        return False
