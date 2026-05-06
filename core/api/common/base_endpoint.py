from core.api.actions.get_actions import GETActions
from core.api.actions.post_actions import POSTActions
from core.api.actions.put_actions import PUTActions
from core.api.actions.delete_actions import DELETEActions
from core.api.actions.patch_actions import PatchAction
from requests import Session

class BaseEndpoint:
    """
    Foundational Base class for all Endpoint Objects within the framework.
    Aggregates specialized HTTP action components.
    """
    def __init__(self, session: Session):
        """
        Initializes the Endpoint Object and its delegated action components.
        
        Args:
            session (Session): The requests Session instance.
        """
        self.session = session
        
        # Action Component Initialization
        self.get = GETActions(self.session)
        self.post = POSTActions(self.session)
        self.put = PUTActions(self.session)
        self.delete = DELETEActions(self.session)
        self.patch = PatchAction(self.session)

    def set_base_url(self, url: str):
        self.base_url = url
        return self
