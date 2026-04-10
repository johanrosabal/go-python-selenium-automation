from core.ui.common.base_app import BaseApp
from applications.web.go_hotel.pages.login.login_page import LoginPage
from applications.web.go_hotel.pages.dashboard.dashboard_page import DashboardPage
from applications.web.go_hotel.pages.reserved.reserved_page import ReservedPage

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

    @property
    def dashboard_page(self) -> DashboardPage:
        """Lazy-loaded instance of DashboardPage."""
        if not hasattr(self, "_dashboard_page") or self._dashboard_page is None:
            self._dashboard_page = DashboardPage()
        return self._dashboard_page

    @property
    def reserved_page(self) -> ReservedPage:
        """Lazy-loaded instance of ReservedPage."""
        if not hasattr(self, "_reserved_page") or self._reserved_page is None:
            self._reserved_page = ReservedPage()
        return self._reserved_page
