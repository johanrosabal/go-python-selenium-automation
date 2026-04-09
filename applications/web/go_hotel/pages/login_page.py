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
        self.window.set_zoom_level(100)
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

    def login(self, email=None, password=None):
        user_email = email if email else self.username
        user_pwd = password if password else self.password
        
        self.logger.info(f"Logging in with email: {user_email}")
        return self.enter_email(user_email) \
                   .enter_password(user_pwd) \
                   .click_login()

    def is_login_successful(self) -> bool:
        # Assuming successful login redirects away from login page
        self.pause(seconds=5)
        return "login" not in self.navigation.get_current_url()
