from core.ui.common.base_app import BaseApp
from applications.web.busisness_partners_portal.pages.home_page import HomePage
from applications.web.busisness_partners_portal.pages.login_page import LoginPage
from applications.web.busisness_partners_portal.pages.agency_code_page import AgencyCodePage


class BusisnessPartnersPortalApp(BaseApp):
    """
    Application Orchestrator for the Busisness Partners Portal Project.
    Provides centralized, lazy-loaded access to all Page Objects.
    """

    @property
    def home_page(self) -> HomePage:
        if not hasattr(self, "_home_page") or self._home_page is None:
            self._home_page = HomePage()
        return self._home_page

    @property
    def login_page(self) -> LoginPage:
        if not hasattr(self, "_login_page") or self._login_page is None:
            self._login_page = LoginPage()
        return self._login_page

    @property
    def agency_code_page(self) -> AgencyCodePage:
        if not hasattr(self, "_agency_code_page") or self._agency_code_page is None:
            self._agency_code_page = AgencyCodePage()
        return self._agency_code_page
