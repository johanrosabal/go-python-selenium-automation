from core.utils.db_client import DBClient

class DBManager:
    """
    Application-specific database manager for Saucedemo.
    """
    def __init__(self):
        self.client = DBClient()

    def get_user_by_username(self, username: str):
        """
        Example query to fetch a user from the database.
        
        Args:
            username (str): The username to search for.
            
        Returns:
            dict: The first user found, or None.
        """
        query = "SELECT * FROM users WHERE username = :username"
        result = self.client.execute_query(query, {"username": username})
        return result[0] if result else None

    def create_test_data(self):
        """
        Example of seeding data before a test.
        """
        query = "INSERT INTO users (username, password) VALUES ('test_user', 'test_pass')"
        self.client.execute_query(query)

    def cleanup_test_data(self):
        """
        Example of cleaning up data after a test.
        """
        query = "DELETE FROM users WHERE username = 'test_user'"
        self.client.execute_query(query)
