from applications.web.demo2.tests.base_test import Demo2BaseTest

class TestWikipedia(Demo2BaseTest):
    """
    Test Suite for Wikipedia interactions.
    """
    
    def test_search_automation(self):
        """
        Scenario: Search for 'Test automation' on Wikipedia.
        """
        # Open Wikipedia (uses base_url from qa.yaml)
        self.app.home_page.open()
        
        # Search for a term
        self.app.home_page.search_for("Test automation")
        
        # Verify the article title
        title = self.app.home_page.get_article_title()
        
        assert "Test automation" in title, f"Expected 'Test automation' but got {title}"
