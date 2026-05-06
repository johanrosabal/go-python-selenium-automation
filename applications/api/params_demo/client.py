from applications.api.params_demo.endpoints.social_endpoint import SocialEndpoint

class ParamsDemoClient:
    """
    App Orchestrator for the params_demo project.
    Provides lazy-loaded access to all endpoints.
    Instantiated automatically by BaseAPITest as self.app.
    """

    def __init__(self, session):
        self._session = session
        self._social = None

    @property
    def social(self) -> SocialEndpoint:
        """Lazy-loaded SocialEndpoint."""
        if self._social is None:
            self._social = SocialEndpoint(self._session)
        return self._social

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def fetch_all_related(self, post_id, user_id):
        """Fetches post, its comments, and the author's albums in one call."""
        return {
            "post":     self.social.get_post(post_id),
            "comments": self.social.get_comments(post_id),
            "albums":   self.social.get_user_albums(user_id),
        }
