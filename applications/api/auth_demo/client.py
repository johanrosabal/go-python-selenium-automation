from applications.api.auth_demo.endpoints.user_auth_endpoint import UserAuthEndpoint

class AuthDemoClient:
    """
    App Orchestrator for the auth_demo project.
    Provides lazy-loaded access to all endpoints.
    Instantiated automatically by BaseAPITest as self.app.
    """

    def __init__(self, session, config: dict):
        self._session = session
        self._token = config.get("token", "")
        self._user_auth = None

    @property
    def user_auth(self) -> UserAuthEndpoint:
        """Lazy-loaded UserAuthEndpoint."""
        if self._user_auth is None:
            self._user_auth = UserAuthEndpoint(self._session)
        return self._user_auth

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def create_and_verify_user(self, name, email, gender="male", status="active"):
        """Creates a user then verifies the list is non-empty."""
        create = self.user_auth.create_user(self._token, name, email, gender, status)
        create.assert_status_code(201)
        listing = self.user_auth.get_users(self._token)
        listing.assert_status_code(200)
        return {"create": create, "list": listing}
