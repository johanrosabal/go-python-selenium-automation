from core.ui.common.base_test import BaseTest
from core.utils.decorators import test_case
from applications.web.demo.utils.decorators import demo

@demo
class TestAppWrapper(BaseTest):
    
    @test_case(id="CT-LOGIN-001")
    def test_login_flow_with_app_wrapper(self):
        """
        Verifies the App Orchestrator pattern.
        Note: No direct imports of LoginPage or InventoryPage are needed.
        """
        data = self.get_data_for_test()
        
        # Using the single 'app' entry point
        self.app.login_page.open().login(data.get("user"), data.get("pass"))
        
        # Accessing another page via the same orchestrator
        assert self.app.inventory_page.is_title_visible()
        self.app.inventory_page.add_backpack_to_cart()
