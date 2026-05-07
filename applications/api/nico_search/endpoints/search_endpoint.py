from core.api.common.base_endpoint import BaseEndpoint


class SearchEndpoint(BaseEndpoint):
    """
    Endpoint for Policy Search and Results (nico_search project).
    Uses the Legacy Builder Style for all requests.
    """

    def __init__(self, session, config):
        super().__init__(session)
        self.base_url = config.get("base_url")
        self.token = config.get("token")

    def search_policies(self, payload):
        """
        Initiates a policy search.
        POST /api/policy-search
        """
        return (
            self.post.set_url(self.base_url)
            .set_endpoint("/api/policy-search")
            .add_header("accept", "text/plain")
            .add_header("Content-Type", f"application/json")
            .add_header("Authorization", f"Bearer {self.token}")
            .set_json(payload)
            .send()
        )

    def get_results(self, search_id):
        """
        Retrieves results for a given search ID.
        GET /api/policy-search/{id}/results
        """
        return (
            self.get.set_url(self.base_url)
            .set_endpoint("/api/policy-search/{id}/results")
            .build_url(id=search_id)
            .add_header("accept", "text/plain")
            .add_header("Authorization", f"Bearer {self.token}")
            .set_timeout(120)
            .send()
        )
