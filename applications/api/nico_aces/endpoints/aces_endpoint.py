from core.api.common.base_endpoint import BaseEndpoint


class AcesEndpoint(BaseEndpoint):
    """
    Endpoint for ACES Policy Search and Results.
    """

    def __init__(self, session, config):
        super().__init__(session)
        self.base_url = config.get("base_url")
        self.token = config.get("token")

        return (
            self.post.set_url(self.base_url)
            .set_endpoint("/api/policies/policy-search")
            .add_header("accept", "application/json")
            .add_header("Authorization", f"Bearer {self.token}")
            .set_json(payload)
            .set_timeout(120)
            .set_verify(False)
            .send()
        )

    def get_policies(self, search_id):
        """
        Retrieves policies for a given search ID in ACES.
        GET /api/policies/policy-search/{id}/policies
        """
        return (
            self.get.set_url(self.base_url)
            .set_endpoint("/api/policies/policy-search/{id}/policies")
            .build_url(id=search_id)
            .add_header("accept", "application/json")
            .add_header("Authorization", f"Bearer {self.token}")
            .set_timeout(120)
            .set_verify(False)
            .send()
        )
