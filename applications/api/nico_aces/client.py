from applications.api.nico_aces.endpoints.aces_endpoint import AcesEndpoint

class NicoAcesClient:
    """
    App Orchestrator for the nico_aces project.
    """

    def __init__(self, session, config: dict):
        self._session = session
        self._config = config
        self._aces = None

    @property
    def aces(self) -> AcesEndpoint:
        """Lazy-loaded AcesEndpoint."""
        if self._aces is None:
            self._aces = AcesEndpoint(self._session, self._config)
        return self._aces

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def search_and_get_policies(self, payload: dict):
        """
        Full flow: POST to initiate search → GET policies by ID.
        """
        search_response = self.aces.search_policies(payload)
        if search_response.status_code != 201 and search_response.status_code != 200:
            return None, search_response

        # Assuming the search_id is returned in the body (adjust if it's in a JSON field)
        search_id = search_response.body.strip()
        results_response = self.aces.get_policies(search_id)
        return search_id, results_response
