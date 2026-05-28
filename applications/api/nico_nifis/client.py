from applications.api.nico_nifis.endpoints.nifis_endpoint import NifisEndpoint

class NicoNifisClient:
    """
    App Orchestrator for the nico_nifis project.
    """

    def __init__(self, session, config: dict):
        self._session = session
        self._config = config
        self._nifis = None

    @property
    def nifis(self) -> NifisEndpoint:
        """Lazy-loaded NifisEndpoint."""
        if self._nifis is None:
            self._nifis = NifisEndpoint(self._session, self._config)
        return self._nifis

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def search_and_get_policies(self, payload: dict):
        """
        Full flow: POST to initiate search -> GET policies by ID.
        """
        search_response = self.nifis.search_policies(payload)
        if search_response.status_code != 201 and search_response.status_code != 200:
            return None, search_response

        # Convert search_id to string in case it is returned as an integer
        search_id = str(search_response.body).strip()
        results_response = self.nifis.get_policies(search_id)
        return search_id, results_response
