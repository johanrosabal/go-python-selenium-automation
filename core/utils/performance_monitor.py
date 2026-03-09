import os
import json
from core.utils.logger_config import setup_logger

class PerformanceMonitor:
    """
    Utility for capturing browser performance metrics (Navigation Timing API).
    """
    def __init__(self, driver):
        self.driver = driver
        self.logger = setup_logger("PerformanceMonitor")
        self.report_dir = os.path.abspath("reports/performance")
        os.makedirs(self.report_dir, exist_ok=True)

    def capture_metrics(self, page_name: str) -> dict:
        """
        Extracts performance metrics from the browser.
        """
        self.logger.info(f"Capturing performance metrics for: {page_name}")
        
        try:
            # Execute JS to get performance timing
            script = "return window.performance.timing.toJSON();"
            timing = self.driver.execute_script(script)
            
            # Calculate more readable metrics (in milliseconds)
            metrics = {
                "page_name": page_name,
                "dns_lookup_time": timing['domainLookupEnd'] - timing['domainLookupStart'],
                "connection_time": timing['connectEnd'] - timing['connectStart'],
                "response_time": timing['responseEnd'] - timing['responseStart'],
                "dom_interactive_time": timing['domInteractive'] - timing['navigationStart'],
                "dom_content_loaded_time": timing['domContentLoadedEventEnd'] - timing['navigationStart'],
                "page_load_time": timing['loadEventEnd'] - timing['navigationStart'],
                "raw_timing": timing
            }
            
            self.logger.info(f"Page Load Time ({page_name}): {metrics['page_load_time']}ms")
            self._save_report(metrics, page_name)
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to capture performance metrics: {e}")
            return {}

    def _save_report(self, metrics: dict, page_name: str):
        """Saves metrics to a JSON file."""
        report_path = os.path.join(self.report_dir, f"{page_name}_performance.json")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=4)
            self.logger.info(f"Performance report saved to: {report_path}")
        except Exception as e:
            self.logger.error(f"Failed to save performance report: {e}")
