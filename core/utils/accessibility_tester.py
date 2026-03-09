import json
import os
from axe_selenium_python import Axe
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager

class AccessibilityTester:
    """
    Utility for accessibility testing using Axe-Core.
    Identifies WCAG violations on the current page.
    """
    def __init__(self, driver):
        self.driver = driver
        self.logger = setup_logger("AccessibilityTester")
        self.report_dir = os.path.abspath("reports/accessibility")
        os.makedirs(self.report_dir, exist_ok=True)

    def scan(self, page_name: str) -> dict:
        """
        Scans the current page for accessibility violations.
        
        Args:
            page_name (str): Name of the page being scanned (for reporting).
            
        Returns:
            dict: The full results from Axe.
        """
        self.logger.info(f"Starting A11y scan for page: {page_name}")
        
        try:
            axe = Axe(self.driver)
            # Inject axe-core and run analysis
            axe.inject()
            results = axe.run()
            
            violations = results.get("violations", [])
            num_violations = len(violations)
            
            if num_violations > 0:
                self.logger.error(f"Found {num_violations} accessibility violations on {page_name}!")
                self._save_report(results, page_name)
            else:
                self.logger.info(f"No accessibility violations found on {page_name}.")
            
            return results
        except Exception as e:
            self.logger.error(f"Failed to perform accessibility scan: {e}")
            return {}

    def _save_report(self, results: dict, page_name: str):
        """Saves a JSON report of the violations."""
        report_path = os.path.join(self.report_dir, f"{page_name}_a11y_violations.json")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(results.get("violations", []), f, indent=4)
            self.logger.info(f"A11y violation report saved to: {report_path}")
        except Exception as e:
            self.logger.error(f"Failed to save A11y report: {e}")
            
    def assert_no_violations(self, page_name: str, impact_limit: str = "critical"):
        """
        Asserts that there are no violations with a specific impact or higher.
        
        Args:
            page_name (str): Name of the page.
            impact_limit (str): The lowest impact level to fail on (critical, serious, moderate, minor).
        """
        results = self.scan(page_name)
        violations = results.get("violations", [])
        
        # impact mapping for comparison
        impact_levels = {"minor": 0, "moderate": 1, "serious": 2, "critical": 3}
        limit_val = impact_levels.get(impact_limit.lower(), 3)
        
        filtered_violations = [
            v for v in violations 
            if impact_levels.get(v.get("impact", "minor"), 0) >= limit_val
        ]
        
        if filtered_violations:
            msg = f"Accessibility check failed for {page_name}. {len(filtered_violations)} {impact_limit}+ violations found."
            # Detailed logging for debugger
            for v in filtered_violations:
                self.logger.error(f"Violation: {v['id']} ({v['impact']}) - {v['description']}")
            
            # Here you would typically attach to Allure if available
            raise AssertionError(msg)
