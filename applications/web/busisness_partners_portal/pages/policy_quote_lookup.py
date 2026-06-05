from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class PolicyQuoteLookup(BasePage):
    """Policy and Quote Lookup page interactions."""

    # Locators
    INP_SEARCH = (By.XPATH, "//input[@formcontrolname='searchInputControl']")
    BTN_SEARCH = (
        By.XPATH,
        "//button/span[contains(@class,'label') and contains(text(),'Search')]",
    )

    TAB_POLICY_NUMBER = (By.XPATH, "//button[contains(text(),'Policy #')]")
    TAB_INSURED_NAME = (By.XPATH, "//button[contains(text(),'Insured Name')]")
    TAB_QUOTE_NUMBER = (By.XPATH, "//button[contains(text(),'Quote #')]")

    LINK_ADVANCED_SEARCH = (By.XPATH, "//a[contains(text(),'Advanced Search')]")

    ERROR_MSG = (By.XPATH, "//div[contains(@class,'policy-filter-error')]")
    TABLE_RESULTS = "//table[contains(@role,'table')]"
    SPINNER = (By.XPATH, "//div[contains(text(), 'Loading Data...')]")
    PROFILE_INFO = (
        By.XPATH,
        "//button[contains(@class,'btn-username')]/span[2]/span[1]",
    )

    def open_home_page(self) -> "PolicyQuoteLookup":
        """Navigates directly to the Policy Lookup endpoint"""
        self.open_relative("/")
        return self

    def open_policy_quote_lookup(self) -> "PolicyQuoteLookup":
        """Navigates directly to the Policy Lookup endpoint"""
        self.open_relative("/tools/policy-search")
        return self

    def type_search_text(self, query: str) -> "PolicyQuoteLookup":
        self.element(self.INP_SEARCH).clear().type(query)
        return self

    def click_search_button(self) -> "PolicyQuoteLookup":
        self.element(self.BTN_SEARCH).click()
        return self

    def click_policy_number_tab(self) -> "PolicyQuoteLookup":
        self.element(self.TAB_POLICY_NUMBER).click()
        return self

    def click_insured_name_tab(self) -> "PolicyQuoteLookup":
        self.element(self.TAB_INSURED_NAME).click()
        return self

    def click_quote_number_tab(self) -> "PolicyQuoteLookup":
        self.element(self.TAB_QUOTE_NUMBER).click()
        return self

    def click_advanced_search_link(self) -> "PolicyQuoteLookup":
        self.element(self.LINK_ADVANCED_SEARCH).click()
        return self

    @allure.step("Entering Policy Number: {policy_number}")
    def search_for_policy_number(self, policy_number: str) -> "PolicyQuoteLookup":
        self.element(self.TAB_POLICY_NUMBER).click()
        self.element(self.INP_SEARCH).clear().type(policy_number)
        self.element(self.BTN_SEARCH).click()
        self.screenshot.full_page("Search by Policy Number")
        return self

    @allure.step("Entering Insured Name: {insured_name}")
    def search_for_insured_name(self, insured_name: str) -> "PolicyQuoteLookup":
        self.element(self.TAB_INSURED_NAME).click()
        self.element(self.INP_SEARCH).clear().type(insured_name)
        self.element(self.BTN_SEARCH).click()
        self.screenshot.full_page("Search by Insured Name")
        return self

    @allure.step("Entering Submission Number: {submission_number}")
    def search_for_quote_number(self, submission_number: str) -> "PolicyQuoteLookup":
        self.element(self.TAB_QUOTE_NUMBER).click()
        self.element(self.INP_SEARCH).clear().type(submission_number)
        self.element(self.BTN_SEARCH).click()
        self.screenshot.full_page("Search by Submission Number")
        return self

    @allure.step("Getting error message")
    def get_error_message(self):
        self.screenshot.full_page("Search Error Message")
        return self.element(self.ERROR_MSG).scroll_to_center().get_text()

    @allure.step("Getting table header from column {column_number}")
    def get_table_header_label(self, column_number: int):
        locator = (By.XPATH, f"{self.TABLE_RESULTS}/thead/tr/th[{column_number}]")
        return self.element(locator).get_text()

    def is_table_displayed(self):
        locator = (By.XPATH, self.TABLE_RESULTS)
        return self.element(locator).is_visible()

    @allure.step("Checking if user is already logged in")
    def is_logged_in(self) -> bool:
        """
        Returns True if the profile info widget is visible, meaning the user is authenticated.
        Uses a short timeout to prevent long waits when the user is NOT logged in.
        """
        return self.element(self.PROFILE_INFO).at(3).is_visible()

    @allure.step("Waiting for login process to finish")
    def wait_for_login_success(self, timeout=60) -> "PolicyQuoteLookup":
        """
        Explicitly waits for the Profile Info widget to appear, indicating successful login.
        """
        self.element(self.PROFILE_INFO).wait_visible(timeout)
        return self

    @allure.step("Waiting for search results to load")
    def wait_for_search_results(self, timeout=15) -> "PolicyQuoteLookup":
        """
        Waits for the loading spinner to appear and disappear,
        and then ensures the results table is populated.
        """
        # 1. Esperamos a que el spinner aparezca (evita condición de carrera)
        try:
            self.element(self.SPINNER).wait_visible(timeout=5)
        except Exception:
            self.logger.info(
                "El spinner fue tan rápido que no se detectó, o ya terminó."
            )

        # 2. Esperamos a que el spinner termine y desaparezca
        self.element(self.SPINNER).wait_disappear(timeout=timeout)

        # 3. Aseguramos que la tabla ya tenga filas dibujadas en el DOM
        locator = (By.XPATH, self.TABLE_RESULTS)
        self.element(locator).table_wait_not_empty(timeout=timeout)
        return self

    @allure.step("Getting the first Policy Number from search results")
    def get_policy_number(self, index=1) -> str:
        """
        Uses the framework's TableActions to dynamically find the 'Policy Number'
        column index by header text, and then returns the value from the first row.
        """
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Policy Number")
            .get_cell_text(row=index, col="Policy #")
        )

    @allure.step("Getting the first Insured Name from search results")
    def get_insured_name(self, index=1) -> str:
        """
        Dynamically finds the 'Insured Name' column and returns the value.
        """
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Insured Name")
            .get_cell_text(row=index, col="Insured Name")
        )

    @allure.step("Getting the first Quote Number from search results")
    def get_quote_number(self, index=1) -> str:
        """
        Dynamically finds the 'Quote Number' column and returns the value.
        """
        locator = (By.XPATH, self.TABLE_RESULTS)
        return (
            self.element(locator)
            .screenshot("Results Quote Number")
            .get_cell_text(row=index, col="Quote #")
        )
