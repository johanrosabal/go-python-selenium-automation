from core.api.common.base_endpoint import BaseEndpoint

class UserEndpoint(BaseEndpoint):
    """
    Endpoint object for User-related operations using reqres.in as a demo.
    """
    def __init__(self, session):
        super().__init__(session)
        self.url = "https://jsonplaceholder.typicode.com/users"

    def get_users(self):
        return self.get.call(self.url)

    def create_user(self, name, job):
        payload = {"name": name, "job": job}
        return self.post.call(self.url, json=payload)

    def get_user_by_id(self, user_id):
        return self.get.call(f"{self.url}/{user_id}")
