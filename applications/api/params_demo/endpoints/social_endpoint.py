from core.api.common.base_endpoint import BaseEndpoint
from core.utils.config_manager import ConfigManager

class SocialEndpoint(BaseEndpoint):
    """Endpoint object demonstrating Path and Query parameters."""
    
    def __init__(self, session):
        super().__init__(session)
        self.base_url = ConfigManager.get("api.base_url")

    def get_post(self, post_id):
        """
        Example of Path Parameter.
        URL: https://.../posts/{id}
        """
        url = f"{self.base_url}/posts/{post_id}"
        return self.get.call(url)

    def get_comments(self, post_id):
        """
        Example of Query Parameter.
        URL: https://.../comments?postId={id}
        """
        url = f"{self.base_url}/comments"
        params = {"postId": post_id}
        return self.get.call(url, params=params)

    def get_user_albums(self, user_id):
        """
        Example of Nested Path Parameter.
        URL: https://.../users/{id}/albums
        """
        url = f"{self.base_url}/users/{user_id}/albums"
        return self.get.call(url)
