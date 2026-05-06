from core.api.common.base_endpoint import BaseEndpoint
from core.utils.config_manager import ConfigManager

class UserAuthEndpoint(BaseEndpoint):
    """Endpoint for User management requiring authentication."""
    
    def __init__(self, session):
        super().__init__(session)
        self.endpoint_path = "/users"
        self.base_url = ConfigManager.get("api.base_url")

    def get_users(self, token, page=1, per_page=10):
        """Get list of users using Bearer token."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        params = {"_page": page, "_limit": per_page} # jsonplaceholder uses _page/_limit
        url = self.base_url + self.endpoint_path
        return self.get.call(url, params=params, headers=headers)

    def create_user(self, token, name, email, gender, status):
        """Create a user (requires valid token)."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": name,
            "email": email,
            "gender": gender,
            "status": status
        }
        url = self.base_url + self.endpoint_path
        return self.post.call(url, json=payload, headers=headers)
