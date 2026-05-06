from core.api.common.base_endpoint import BaseEndpoint
from core.utils.config_manager import ConfigManager

class MasterEndpoint(BaseEndpoint):
    """Universal Endpoint object for advanced API demonstrations."""
    
    def __init__(self, session):
        super().__init__(session)
        self.base_url = ConfigManager.get("api.base_url")
        self.reqres_url = ConfigManager.get("api.reqres_url")
        self.token = ConfigManager.get("api.token")

    # --- CRUD Operations ---
    
    def get_users(self):
        """GET list of users."""
        return self.get.call(f"{self.base_url}/users")

    def get_user_by_id(self, user_id):
        """GET a single user by path parameter."""
        return self.get.call(f"{self.base_url}/users/{user_id}")

    def create_user(self, name, job):
        """POST to create a new user (using ReqRes)."""
        payload = {"name": name, "job": job}
        return self.post.call(f"{self.reqres_url}/users", json=payload)

    def update_user(self, user_id, name, job):
        """PUT to update a user (Full update)."""
        payload = {"name": name, "job": job}
        return self.put.call(f"{self.reqres_url}/users/{user_id}", json=payload)

    def patch_user(self, user_id, job):
        """PATCH to update partial data."""
        payload = {"job": job}
        # In our core, we need to ensure PATCH is implemented. Let's check.
        # If not, we'll use PUT as proxy or implement it.
        if hasattr(self, 'patch'):
            return self.patch.call(f"{self.reqres_url}/users/{user_id}", json=payload)
        return self.put.call(f"{self.reqres_url}/users/{user_id}", json=payload)

    def delete_user(self, user_id):
        """DELETE a user."""
        return self.delete.call(f"{self.reqres_url}/users/{user_id}")

    # --- Advanced Scenarios ---

    def get_with_custom_headers(self, custom_headers):
        """GET with specialized headers."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Custom-Request-ID": "MASTER-123",
            **custom_headers
        }
        return self.get.call(f"{self.base_url}/posts/1", headers=headers)

    def get_filtered_comments(self, post_id, limit=5):
        """GET with multiple query parameters."""
        params = {"postId": post_id, "_limit": limit}
        return self.get.call(f"{self.base_url}/comments", params=params)

    def force_error(self, status_code):
        """Call a non-existent route to force a 404, or httpbin for other codes."""
        if status_code == 404:
            return self.get.call(f"{self.base_url}/non-existent-route-999")
        return self.get.call(f"https://httpbin.org/status/{status_code}")
