from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class PolicyLookupAdvancePage(BasePage):
    """Policy Lookup Advance Page interactions."""

    # Locators
    INP_POLICY_NUMBER = (
        By.XPATH,
        "//label[contains(text(),'Policy Number')]/..//input",
    )
    TXT_POLICY_NUMBER_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'Policy Number')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The policy number should contain 3 to 14 characters

    INP_INSURED_NAME = (By.XPATH, "//label[contains(text(),'Insured Name')]/..//input")
    TXT_INSURED_NAME_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'Insured Name')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The insured name should contain 50 characters or less

    INP_SUBMISSION_NUMBER = (
        By.XPATH,
        "//label[contains(text(),'Submission Number')]/..//input",
    )
    TXT_SUBMISSION_NUMBER_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'Submission Number')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The submission number should only have numbers

    INP_EFFECTIVE_DATE = (
        By.XPATH,
        "//label[contains(text(),'Effective Date')]/..//input",
    )
    TXT_EFFECTIVE_DATE_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'Effective Date')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The effective date must not be after 6/9/2027

    INP_INSURED_PHONE_NUMBER = (
        By.XPATH,
        "//label[contains(text(),'Insured Phone Number')]/..//input",
    )
    TXT_INSURED_PHONE_NUMBER_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'Insured Phone Number')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The insured phone number should contain 3 to 10 digits

    INP_VIN = (By.XPATH, "//label[contains(text(),'VIN')]/..//input")
    TXT_VIN_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'VIN')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The VIN should contain 3 to 17 characters

    TXT_POLICY_STATE = (By.XPATH, "//label[contains(text(),'Policy State')]/../div/div")
    SELECT_ITEM = (
        By.XPATH,
        "//label[contains(text(),'Policy State')]/..//li[contains(text(),'{state}')]",
    )

    INP_INSURED_EMAIL_ADDRESS = (
        By.XPATH,
        "//label[contains(text(),'Insured Email Address')]/..//input",
    )
    TXT_INSURED_EMAIL_ADDRESS_ERROR_MSG = (
        By.XPATH,
        "//label[contains(text(),'Insured Email Address')]/..//div[contains(@class,'validation-message')]",
    )
    # Error Message Validation: The insured email address should contain 3 to 50 characters

    BTN_SEARCH = (By.XPATH, "//button[contains(text(),'Search')]")
    BTN_CLEAR = (By.XPATH, "//button[contains(text(), 'Clear')]")

    TABLE_RESULTS = "//table[contains(@class,'results')]"
    SPINNER = (By.XPATH, "//div[contains(@class,'spinner-policy-search')]")

    def open_policy_advanced_search(self) -> "PolicyLookupAdvancePage":
        """Navigates directly to the Policy Advance Search endpoint"""
        self.open_relative("/policy-advanced-search")
        return self

    @allure.step("Entering Policy Number: {policy_number}")
    def type_policy_number(self, policy_number: str) -> "PolicyLookupAdvancePage":
        self.element(self.INP_POLICY_NUMBER).wait_visible().clear().type(policy_number)
        return self

    @allure.step("Entering Insured Name: {insured_name}")
    def type_insured_name(self, insured_name: str) -> "PolicyLookupAdvancePage":
        self.element(self.INP_INSURED_NAME).wait_visible().clear().type(insured_name)
        return self

    @allure.step("Entering Submission Number: {submission_number}")
    def type_submission_number(
        self, submission_number: str
    ) -> "PolicyLookupAdvancePage":
        self.element(self.INP_SUBMISSION_NUMBER).wait_visible().clear().type(
            submission_number
        )
        return self

    @allure.step("Entering Effective Date: {effective_date}")
    def type_effective_date(self, effective_date: str) -> "PolicyLookupAdvancePage":
        self.element(self.INP_EFFECTIVE_DATE).wait_visible().clear().type(
            effective_date
        )
        return self

    @allure.step("Entering Insured Phone Number: {phone_number}")
    def type_insured_phone_number(self, phone_number: str) -> "PolicyLookupAdvancePage":
        self.element(self.INP_INSURED_PHONE_NUMBER).wait_visible().clear().type(
            phone_number
        )
        return self

    @allure.step("Entering VIN: {vin}")
    def type_vin(self, vin: str) -> "PolicyLookupAdvancePage":
        self.element(self.INP_VIN).wait_visible().clear().type(vin)
        return self

    @allure.step("Selecting Policy State: {option}")
    def select_policy_state(self, option: str) -> "PolicyLookupAdvancePage":
        self.element(self.TXT_POLICY_STATE).wait_visible().click()
        ITEM_OPTION = (self.SELECT_ITEM[0], self.SELECT_ITEM[1].format(state=option))
        self.element(ITEM_OPTION).wait_present().click()
        return self

    @allure.step("Entering Insured Email Address: {email}")
    def type_insured_email_address(self, email: str) -> "PolicyLookupAdvancePage":
        self.element(self.INP_INSURED_EMAIL_ADDRESS).wait_visible().clear().type(email)
        return self

    @allure.step("Clicking Search button")
    def click_search_button(self) -> "PolicyLookupAdvancePage":
        self.element(self.BTN_SEARCH).click()
        return self

    @allure.step("Clicking Clear button")
    def click_clear_button(self) -> "PolicyLookupAdvancePage":
        self.element(self.BTN_CLEAR).click().pause(3)
        return self

    @allure.step("Waiting for search results to load")
    def wait_for_search_results(self, timeout=15) -> "PolicyLookupAdvancePage":
        try:
            self.element(self.SPINNER).wait_visible(timeout=5)
        except Exception:
            self.logger.info(
                "El spinner fue tan rápido que no se detectó o ya terminó."
            )
        self.element(self.SPINNER).wait_disappear(timeout=timeout)
        locator = (By.XPATH, self.TABLE_RESULTS)
        self.element(locator).table_wait_not_empty(timeout=timeout)
        return self

    def is_table_displayed(self) -> bool:
        locator = (By.XPATH, self.TABLE_RESULTS)
        return self.element(locator).is_visible()

    @allure.step("Getting the Policy Number from search results")
    def get_policy_number(self, index=1) -> str:
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Policy Number")
            .get_cell_text(row=index, col="Policy Number")
        )

    @allure.step("Getting the Insured Name from search results")
    def get_insured_name(self, index=1) -> str:
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Insured Name")
            .get_cell_text(row=index, col="Insured Name")
        )

    @allure.step("Getting the Submission Number from search results")
    def get_submission_number(self, index=1) -> str:
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Submission Number")
            .get_cell_text(row=index, col="Submission Number")
        )

    # Error Message Getters
    @allure.step("Getting policy number error message")
    def get_policy_number_error_message(self) -> str:
        return self.element(self.TXT_POLICY_NUMBER_ERROR_MSG).get_text()

    @allure.step("Getting insured name error message")
    def get_insured_name_error_message(self) -> str:
        return self.element(self.TXT_INSURED_NAME_ERROR_MSG).get_text()

    @allure.step("Getting submission number error message")
    def get_submission_number_error_message(self) -> str:
        return self.element(self.TXT_SUBMISSION_NUMBER_ERROR_MSG).get_text()

    @allure.step("Getting effective date error message")
    def get_effective_date_error_message(self) -> str:
        return self.element(self.TXT_EFFECTIVE_DATE_ERROR_MSG).get_text()

    @allure.step("Getting insured phone number error message")
    def get_insured_phone_number_error_message(self) -> str:
        return self.element(self.TXT_INSURED_PHONE_NUMBER_ERROR_MSG).get_text()

    @allure.step("Getting VIN error message")
    def get_vin_error_message(self) -> str:
        return self.element(self.TXT_VIN_ERROR_MSG).get_text()

    @allure.step("Getting insured email address error message")
    def get_insured_email_address_error_message(self) -> str:
        return self.element(self.TXT_INSURED_EMAIL_ADDRESS_ERROR_MSG).get_text()
