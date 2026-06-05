from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
from core.utils.interactive_prompt import ask_for_mfa_code
import allure


class LoginPage(BasePage):
    """Page Object for Microsoft Login and Okta MFA handling."""

    # Locators
    INP_EMAIL = (By.XPATH, "//label[contains(text(),'Username')]/../..//input")
    INP_PASSWORD = (By.XPATH, "//label[contains(text(),'Password')]/../..//input")
    BTN_NEXT = (By.XPATH, "//input[@value='Sign In']")

    # Okta Locator (adjust if different)
    INP_OKTA_CODE = (
        By.XPATH,
        "//label[contains(text(),'Enter Code')]/../..//input",
    )  # This locator will need adjustment based on actual Okta DOM
    BTN_VERIFY_OKTA = (By.XPATH, "//input[@value='Verify']")

    @allure.step("Performing Microsoft Login with Okta MFA")
    def login_microsoft(self, email: str, password: str):
        """
        Executes the Microsoft login flow. It inputs the email, clicks next,
        inputs the password, clicks sign in, and then pauses execution with
        a UI prompt for the user to provide the Okta code (or skip).
        """
        # 1. Enter Email
        self.element(self.INP_EMAIL).type(email)
        self.element(self.BTN_NEXT).click()

        # 2. Enter Password
        self.element(self.INP_PASSWORD).type(password)
        self.element(self.BTN_NEXT).click()

        # 3. Wait for MFA / Ask User
        bypass_okta = self.config.get("credentials.okta.bypass") or False
        if bypass_okta:
            self.logger.info("Okta MFA bypass is enabled. Skipping MFA steps.")
            return self

        self.logger.info(
            "Credentials submitted. Waiting for manual Okta MFA intervention."
        )

        default_okta = self.config.get("credentials.okta.code") or ""
        mfa_code = ask_for_mfa_code(default_code=default_okta)

        if mfa_code:
            self.logger.info(f"Received MFA code from user. Injecting: {mfa_code}")
            # Ensure the Okta code input is visible before typing
            # Adjust these generic locators to the actual Okta elements
            try:
                self.element(self.INP_OKTA_CODE).type(mfa_code)
                self.element(self.BTN_VERIFY_OKTA).click()
            except Exception as e:
                self.logger.error(
                    f"Failed to automatically inject Okta code. Check locators. {e}"
                )
        else:
            self.logger.info("User skipped Okta code injection. Proceeding...")

        # Optional: Handle the 'Stay signed in?' prompt if it appears after Okta
        # self.element(self.BTN_NEXT).click_if_exists()

        return self
