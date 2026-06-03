from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class HomePage(BasePage):
    """Home internal Homepage interactions."""

    # Locators
    INP_SEARCH = (By.XPATH, "//input[@class='policy-search-input']")
    BTN_SEARCH = (By.XPATH, "//button[text()='Search']")

    TAB_POLICY_NUMBER = (By.XPATH, "//button[contains(text(),'Policy Number')]")
    TAB_INSURED_NAME = (By.XPATH, "//button[contains(text(),'Insured Name')]")
    TAB_SUBMISSION_NUMBER = (By.XPATH, "//button[contains(text(),'Submission Number')]")

    LINK_ADVANCED_SEARCH = (By.XPATH, "//a[contains(text(),'Advanced Search')]")

    def type_search_text(self, query: str):
        self.element(self.INP_SEARCH).clear().type(query)

    def click_search_button(self):
        self.element(self.BTN_SEARCH).click()

    def click_policy_number_tab(self):
        self.element(self.TAB_POLICY_NUMBER).click()

    def click_insured_name_tab(self):
        self.element(self.TAB_INSURED_NAME).click()

    def click_submission_number_tab(self):
        self.element(self.TAB_SUBMISSION_NUMBER).click()

    def click_advanced_search_link(self):
        self.element(self.LINK_ADVANCED_SEARCH).click()

    @allure.step("Entering Policy Number: {policy_number}")
    def search_for_policy_number(self, policy_number: str):
        self.element(self.TAB_POLICY_NUMBER).click()
        self.element(self.INP_SEARCH).clear().type(policy_number)
        self.element(self.BTN_SEARCH).click()

    @allure.step("Entering Insured Name: {insured_name}")
    def search_for_insured_name(self, insured_name: str):
        self.element(self.TAB_INSURED_NAME).click()
        self.element(self.INP_SEARCH).clear().type(insured_name)
        self.element(self.BTN_SEARCH).click()

    @allure.step("Entering Submission Number: {submission_number}")
    def search_for_submission_number(self, submission_number: str):
        self.element(self.TAB_SUBMISSION_NUMBER).click()
        self.element(self.INP_SEARCH).clear().type(submission_number)
        self.element(self.BTN_SEARCH).click()
