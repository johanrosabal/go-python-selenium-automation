from core.ui.common.base_app import BaseApp
from applications.web.demo.pages.login_page import LoginPage
from applications.web.demo.pages.inventory_page import InventoryPage
from applications.web.demo.app.db_manager import DBManager

class DemoApp(BaseApp):
    """
    App Orchestrator for the Demo application.
    
    This class centralizes access to all Page Objects, providing
    lazy loading and ensuring a single entry point for tests.
    """
    
    @property
    def db(self) -> DBManager:
        """Lazy-loaded instance of DBManager."""
        if not hasattr(self, "_db") or self._db is None:
            self._db = DBManager()
        return self._db

    @property
    def login_page(self) -> LoginPage:
        """Lazy-loaded instance of LoginPage."""
        if not hasattr(self, "_login_page") or self._login_page is None:
            self._login_page = LoginPage()
        return self._login_page

    @property
    def inventory_page(self) -> InventoryPage:
        """Lazy-loaded instance of InventoryPage."""
        if not hasattr(self, "_inventory_page") or self._inventory_page is None:
            self._inventory_page = InventoryPage()
        return self._inventory_page
