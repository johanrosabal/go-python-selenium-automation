from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By

class WikiHomePage(BasePage):
    """Wikipedia internal Homepage interactions."""
    
    # Locators
    INP_SEARCH = (By.ID, "searchInput")
    BTN_SEARCH = (By.CSS_SELECTOR, "button[type='submit']")
    LBL_HEADING = (By.ID, "firstHeading")

    def search_for(self, query: str):
        """Perform a search on Wikipedia."""
        self.element(self.INP_SEARCH).type(query)
        self.element(self.BTN_SEARCH).click()
        return self

    def get_article_title(self) -> str:
        """Get the title of the current article."""
        return self.element(self.LBL_HEADING).get_text()
