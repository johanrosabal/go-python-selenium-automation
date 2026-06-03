from core.utils.test_decorators import project_config
from applications.web.demo.app.demo_app import DemoApp

def demo(cls):
    """
    Decorator to configure default parameters for the 'demo' application tests.
    Wraps the core project_config decorator to maintain backwards compatibility.
    """
    cls.profile = "qa"
    cls.browser = "chrome"
    return project_config(app_name="demo", app_class=DemoApp)(cls)

