from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class PolicyAdvanceSearchPage(BasePage):
    """Policy and Quote Lookup page interactions."""

    # Locators
    INP_POLICY_NUMBER = (
        By.XPATH,
        "//label/mat-label[contains(text(),'Policy Number')]/../..//input",
    )
    INP_INSURED_NAME = (
        By.XPATH,
        "//label/mat-label[contains(text(),'Insured Name')]/../..//input",
    )
    INP_QUOTE_NUMBER = (
        By.XPATH,
        "//label/mat-label[contains(text(),'Quote Number')]/../..//input",
    )
    INP_EFFECTIVE_DATE = (
        By.XPATH,
        "//label/mat-label[contains(text(),'Effective Date')]/../..//input",
    )
    INP_INSURED_PHONE_NUMBER = (
        By.XPATH,
        "//label/mat-label[contains(text(),'Insured Phone Number')]/../..//input",
    )
    INP_VIN = (By.XPATH, "//label/mat-label[contains(text(),'VIN')]/../..//input")
    TXT_POLICY_STATE = (By.XPATH, "//span[contains(text(),'Policy State')]/../..")
    INP_INSURED_EMAIL_ADDRESS = (
        By.XPATH,
        "//label/mat-label[contains(text(),'Insured Email Address')]/../..//input",
    )
    BTN_SEARCH = (
        By.XPATH,
        "//button/span[contains(@class,'label') and contains(text(),'Search')]",
    )
    BTN_CLEAR = (
        By.XPATH,
        "//button/span[contains(@class,'label') and contains(text(),'Clear')]",
    )

    TABLE_RESULTS = "//table[contains(@role,'table')]"
    SPINNER = (By.XPATH, "//div[contains(text(), 'Loading Data...')]")

    def open_policy_advance(self) -> "PolicyAdvanceSearchPage":
        """Navigates directly to the Policy Lookup endpoint"""
        self.open_relative("/tools/policy-search")
        return self

    @allure.step("Entering Policy Number: {policy_number}")
    def type_policy_number(self, policy_number: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_POLICY_NUMBER).wait_visible().clear().type(policy_number)
        return self

    @allure.step("Entering Insured Name: {insured_name}")
    def type_insured_name(self, insured_name: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_INSURED_NAME).wait_visible().clear().type(insured_name)
        return self

    @allure.step("Entering Quote Number: {quote_number}")
    def type_quote_number(self, quote_number: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_QUOTE_NUMBER).wait_visible().clear().type(quote_number)
        return self

    @allure.step("Entering Effective Date: {effective_date}")
    def type_effective_date(self, effective_date: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_EFFECTIVE_DATE).wait_visible().clear().type(effective_date)
        return self

    @allure.step("Entering Insured Phone Number: {phone_number}")
    def type_insured_phone_number(self, phone_number: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_INSURED_PHONE_NUMBER).wait_visible().clear().type(phone_number)
        return self

    @allure.step("Entering VIN: {vin}")
    def type_vin(self, vin: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_VIN).wait_visible().clear().type(vin)
        return self

    @allure.step("Entering Policy State: {vin}")
    def select_policy_state(self, option: str) -> "PolicyAdvanceSearchPage":
        ITEM_OPTION = (By.XPATH, f"//mat-option/span[contains(text(),'{option}')]")
        self.element(self.TXT_POLICY_STATE).wait_visible().click()
        self.element(ITEM_OPTION).wait_present().click()
        return self

    @allure.step("Entering Insured Email Address: {email}")
    def type_insured_email_address(self, email: str) -> "PolicyAdvanceSearchPage":
        self.element(self.INP_INSURED_EMAIL_ADDRESS).wait_visible().clear().type(email)
        return self

    @allure.step("Clicking Search button")
    def click_search_button(self) -> "PolicyAdvanceSearchPage":
        self.element(self.BTN_SEARCH).click()
        return self

    @allure.step("Clicking Clear button")
    def click_clear_button(self) -> "PolicyAdvanceSearchPage":
        self.element(self.BTN_CLEAR).click()
        return self

    @allure.step("Waiting for search results to load")
    def wait_for_search_results(self, timeout=15) -> "PolicyAdvanceSearchPage":
        """
        Waits for the loading spinner to appear and disappear,
        and then ensures the results table is populated.
        """
        try:
            self.element(self.SPINNER).wait_visible(timeout=5)
        except Exception:
            self.logger.info(
                "El spinner fue tan rápido que no se detectó, o ya terminó."
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
            .get_cell_text(row=index, col="Policy #")
        )

    @allure.step("Getting the Insured Name from search results")
    def get_insured_name(self, index=1) -> str:
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Insured Name")
            .get_cell_text(row=index, col="Insured Name")
        )

    @allure.step("Getting the Quote Number from search results")
    def get_quote_number(self, index=1) -> str:
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Quote Number")
            .get_cell_text(row=index, col="Quote #")
        )
