import pytest
from core.ui.common.base_test import BaseTest
from core.utils.decorators import test_case

class TestDatabaseIntegration(BaseTest):
    """
    Verification tests for database integration.
    """
    
    @test_case(id="DB-VERIFY-001")
    def test_database_connection(self):
        # 1. Seed data using the orchestrator
        self.app.db.client.execute_query(
            "INSERT INTO users (username, password) VALUES ('db_admin', 'secret_db_123')"
        )
        
        # 2. Query data using DBManager
        user = self.app.db.get_user_by_username("db_admin")
        
        # 3. Verify
        assert user is not None, "User should be found in the database"
        assert user["password"] == "secret_db_123", f"Unexpected password: {user['password']}"
        
        # 4. Cleanup
        self.app.db.client.execute_query("DELETE FROM users WHERE username = 'db_admin'")
        print("\nDatabase verification successful!")
