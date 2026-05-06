from applications.api.master_suite.endpoints.master_endpoint import MasterEndpoint

class MasterClient:
    """
    App Orchestrator for the master_suite project.
    Provides lazy-loaded access to all endpoints.
    Instantiated automatically by BaseAPITest as self.app.
    """

    def __init__(self, session):
        self._session = session
        self._master = None

    @property
    def master(self) -> MasterEndpoint:
        """Lazy-loaded MasterEndpoint."""
        if self._master is None:
            self._master = MasterEndpoint(self._session)
        return self._master

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def full_crud_flow(self, name, job):
        """
        Executes a complete CRUD lifecycle: Create → Read → Update → Delete.
        Returns a dict with each response for individual assertions.
        """
        create = self.master.create_user(name, job)
        create.assert_status_code(201)
        user_id = create.body.get("id", 1)

        return {
            "create": create,
            "read":   self.master.get_user_by_id(user_id),
            "update": self.master.update_user(user_id, name, "Senior " + job),
            "delete": self.master.delete_user(user_id),
        }
