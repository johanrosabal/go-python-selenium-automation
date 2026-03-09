from core.utils.cleaner import Cleaner

def pytest_sessionstart(session):
    """
    Hooks into the start of the pytest session to perform cleanup.
    """
    Cleaner.clean_reports()

def pytest_sessionfinish(session, exitstatus):
    """
    Hooks into the end of the pytest session to send notifications.
    """
    from core.utils.notifier import Notifier
    from core.utils.config_manager import ConfigManager
    
    # Get statistics from the session
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    passed = len(reporter.stats.get("passed", []))
    failed = len(reporter.stats.get("failed", []))
    xfailed = len(reporter.stats.get("xfailed", []))
    skipped = len(reporter.stats.get("skipped", []))
    total = passed + failed + xfailed + skipped
    
    try:
        project_name = ConfigManager.get("metadata.project_name", "QA Automation")
    except ValueError:
        project_name = "QA Automation"
    
    notifier = Notifier()
    notifier.send_summary(
        project_name=project_name,
        total=total,
        passed=passed,
        failed=failed
    )
