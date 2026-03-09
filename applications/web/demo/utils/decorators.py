def demo(cls):
    """
    Decorator to configure default parameters for the 'demo' application tests.
    These values serve as defaults for local runs (IDEs) but do not override 
    explicit environment variables.
    """
    cls.profile = "qa"
    cls.app_name = "demo"
    cls.app_type = "web"
    cls.browser = "chrome"
    return cls
