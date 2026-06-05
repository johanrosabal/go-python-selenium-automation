from core.ui.common.base_app import BaseApp
from applications.web.busisness_partners_portal.pages.policy_quote_lookup import PolicyQuoteLookup
from applications.web.busisness_partners_portal.pages.login_page import LoginPage
from applications.web.busisness_partners_portal.pages.agency_code_page import AgencyCodePage


class BusisnessPartnersPortalApp(BaseApp):
    """
    Application Orchestrator for the Busisness Partners Portal Project.
    Provides centralized, lazy-loaded access to all Page Objects.
    """

    @property
    def policy_quote_lookup(self) -> PolicyQuoteLookup:
        if not hasattr(self, "_policy_quote_lookup") or self._policy_quote_lookup is None:
            self._policy_quote_lookup = PolicyQuoteLookup()
        return self._policy_quote_lookup

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
