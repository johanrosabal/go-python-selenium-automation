from core.ui.common.base_app import BaseApp
from applications.web.go_hotel.pages.login_page import LoginPage

class GoHotelApp(BaseApp):
    """
    App Orchestrator for the Go Hotel application.
    
    This class centralizes access to all Page Objects, providing
    lazy loading and ensuring a single entry point for tests.
    """
    
    @property
    def login_page(self) -> LoginPage:
        """Lazy-loaded instance of LoginPage."""
        if not hasattr(self, "_login_page") or self._login_page is None:
            self._login_page = LoginPage()
        return self._login_page
