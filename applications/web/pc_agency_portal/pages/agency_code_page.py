from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class AgencyCodePage(BasePage):
    """Agency Code Page interactions."""

    # Locators
    SELECT_SEARCH = (By.XPATH, "//div[@class='dropdown']/div")
    TEXT_ITEM_SELECTED = (
        By.XPATH,
        "//div[@class='portal-dropdown-button-text']/span[1]",
    )
    BTN_SUBMIT = (By.XPATH, "//button[text()='Submit']")
    BTN_SIGN_OUT = (By.XPATH, "//div[contains(text(), 'Sign Out')]")

    def click_select_agency_code(self) -> "AgencyCodePage":
        """
        Clicks on the agency code selection dropdown to open the list.
        """
        self.element(self.SELECT_SEARCH).click()
        return self

    def is_visible(self) -> bool:
        """
        Checks if the agency code dropdown is currently visible.
        """
        return self.element(self.SELECT_SEARCH).is_visible()

    def select_item(self, option: str) -> "AgencyCodePage":
        """
        Selects a specific agency code option from the dropdown list.

        Args:
            option (str): The agency code/option text to search and select.
        """
        ITEM = (
            By.XPATH,
            f"//button[@class='dropdown-item']/span[contains(text(),'{option}')]",
        )
        self.element(ITEM).click()
        return self

    def click_submit_agency_code(self) -> "AgencyCodePage":
        """
        Clicks the search/submit button for the selected agency code.
        """
        self.element(self.BTN_SUBMIT).click()
        return self

    def select_an_agency(self, agency: str) -> "AgencyCodePage":
        """
        Performs the complete flow of selecting an agency and submitting it.
        It opens the dropdown, selects the item, takes a screenshot, and submits.

        Args:
            agency (str): The agency code/name to select.
        """
        self.click_select_agency_code()
        self.select_item(agency)
        self.screenshot.full_page(name="Agency Code Selected")
        self.click_submit_agency_code()
        return self

    def get_selected_agency_code(self) -> str:
        """
        Retrieves the text of the currently selected agency code.

        Returns:
            str: The selected agency code text.
        """
        return self.element(self.TEXT_ITEM_SELECTED).get_text()

    def click_signout(self) -> "AgencyCodePage":
        """
        Clicks the sign out option to log out of the portal.
        """
        self.element(self.BTN_SIGN_OUT).click()
        return self
