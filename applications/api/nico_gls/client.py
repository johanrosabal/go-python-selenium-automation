from applications.api.nico_gls.endpoints.gls_endpoint import GlsEndpoint

class NicoGlsClient:
    """
    App Orchestrator for the nico_gls project.
    """

    def __init__(self, session, config: dict):
        self._session = session
        self._config = config
        self._gls = None

    @property
    def gls(self) -> GlsEndpoint:
        """Lazy-loaded GlsEndpoint."""
        if self._gls is None:
            self._gls = GlsEndpoint(self._session, self._config)
        return self._gls

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def search_and_get_policies(self, payload: dict):
        """
        Full flow: POST to initiate search -> GET policies by ID.
        """
        search_response = self.gls.search_policies(payload)
        if search_response.status_code != 201 and search_response.status_code != 200:
            return None, search_response

        # Convert search_id to string in case it is returned as an integer
        search_id = str(search_response.body).strip()
        results_response = self.gls.get_policies(search_id)
        return search_id, results_response
