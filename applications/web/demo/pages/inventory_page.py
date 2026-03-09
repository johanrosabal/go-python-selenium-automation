from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage(BasePage):
    """
    Page Object for the Inventory page (Products page).
    """
    SIDE_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    TITLE = (By.CLASS_NAME, "title")
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")

    def is_title_visible(self) -> bool:
        """
        Checks if the page title is visible.
        """
        return self.element(self.TITLE).is_visible()

    def add_backpack_to_cart(self):
        """
        Clicks the 'Add to cart' button for the backpack.
        """
        self.logger.info("Adding backpack to cart")
        self.element(self.BACKPACK_ADD_BUTTON).click()
        return self

    def logout(self):
        """
        Performs the logout sequence via the sidebar menu.
        """
        self.logger.info("Performing logout")
        self.element(self.SIDE_MENU_BUTTON).click()
        
        # Small delay for sidebar animation
        import time
        time.sleep(0.5)

        # Wait for and click logout link
        self.element(self.LOGOUT_LINK).wait_clickable().click()
        
        # Wait for the login page URL to be reached exactly (handles optional trailing slash)
        expected_url = self.base_url.rstrip("/")
        from selenium.webdriver.support import expected_conditions as EC
        import re
        # Use a more flexible regex to match the base URL with or without a trailing slash
        self.wait.until(EC.url_matches(rf"^{re.escape(expected_url)}/?$"))
        
        # Return LoginPage for chaining if needed
        from applications.web.demo.pages.login_page import LoginPage
        return LoginPage()
