from core.ui.common.base_app import BaseApp
from applications.web.demo2.pages.wiki_home_page import WikiHomePage

class Demo2App(BaseApp):
    """
    Application Orchestrator for the Wikipedia Project.
    Provides centralized, lazy-loaded access to all Page Objects.
    """
    
    @property
    def home_page(self) -> WikiHomePage:
        if not hasattr(self, "_home_page") or self._home_page is None:
            self._home_page = WikiHomePage()
        return self._home_page
