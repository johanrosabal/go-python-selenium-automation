from applications.api.nico_rate.endpoints.rate_endpoint import RateEndpoint

class NicoRateClient:
    """
    App Orchestrator for the nico_rate project.
    """

    def __init__(self, session, config: dict):
        self._session = session
        self._config = config
        self._rate = None

    @property
    def rate(self) -> RateEndpoint:
        """Lazy-loaded RateEndpoint."""
        if self._rate is None:
            self._rate = RateEndpoint(self._session, self._config)
        return self._rate

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def search_and_get_policies(self, payload: dict):
        """
        Full flow: POST to initiate search -> GET policies by ID.
        """
        search_response = self.rate.search_policies(payload)
        if search_response.status_code != 201 and search_response.status_code != 200:
            return None, search_response

        # Convert search_id to string in case it is returned as an integer
        search_id = str(search_response.body).strip()
        results_response = self.rate.get_policies(search_id)
        return search_id, results_response
