from applications.api.nico_search.endpoints.search_endpoint import SearchEndpoint

class NicoSearchClient:
    """
    App Orchestrator for the nico_search project.
    Provides lazy-loaded access to all endpoints.
    Instantiated automatically by BaseAPITest as self.app.
    """

    def __init__(self, session, config: dict):
        self._session = session
        self._config = config
        self._search = None

    @property
    def search(self) -> SearchEndpoint:
        """Lazy-loaded SearchEndpoint."""
        if self._search is None:
            self._search = SearchEndpoint(self._session, self._config)
        return self._search

    # =========================================================================
    # Composed Flows
    # =========================================================================

    def search_and_get_results(self, payload: dict):
        """
        Full flow: POST to initiate search → GET results by GUID.
        Returns: tuple (search_id: str, results_response: APIResponse)
        Note: If search fails, search_id will be None and results_response will be the error response.
        """
        search_response = self.search.search_policies(payload)
        if search_response.status_code != 201:
            return None, search_response

        search_id = search_response.body.strip()
        results_response = self.search.get_results(search_id)
        return search_id, results_response
