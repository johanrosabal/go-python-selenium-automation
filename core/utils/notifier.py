import requests
import json
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager

class Notifier:
    """
    Utility for sending test execution notifications to Slack or MS Teams.
    """
    def __init__(self, webhook_url: str = None):
        self.logger = setup_logger("Notifier")
        
        if webhook_url:
            self.webhook_url = webhook_url
        else:
            try:
                self.webhook_url = ConfigManager.get("notifications.webhook_url")
            except ValueError:
                # Occurs during pytest test discovery when ConfigManager isn't loaded yet
                self.webhook_url = None

    def send_summary(self, project_name: str, total: int, passed: int, failed: int, report_url: str = None):
        """
        Sends a formatted summary to the configured webhook.
        """
        if not self.webhook_url:
            self.logger.warning("No webhook URL configured. Skipping notification.")
            return

        # Determine status emoji
        emoji = "✅" if failed == 0 else "❌"
        status = "PASSED" if failed == 0 else "FAILED"
        
        # Payload for Slack (Universal Block Kit preferred, but simple text works)
        payload = {
            "text": f"*{emoji} Test Execution Summary: {project_name}*",
            "attachments": [
                {
                    "color": "#36a64f" if failed == 0 else "#ec1a1a",
                    "fields": [
                        {"title": "Status", "value": status, "short": True},
                        {"title": "Total Tests", "value": str(total), "short": True},
                        {"title": "Passed", "value": str(passed), "short": True},
                        {"title": "Failed", "value": str(failed), "short": True}
                    ],
                    "footer": "Sent by Antigravity God Tier Framework"
                }
            ]
        }
        
        if report_url:
            payload["attachments"][0]["fields"].append({"title": "Allure Report", "value": f"<{report_url}|View Report>", "short": False})

        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                self.logger.info("Notification sent successfully.")
            else:
                self.logger.error(f"Failed to send notification: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"Error sending notification: {e}")
