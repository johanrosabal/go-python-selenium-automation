def go_hotel(cls):
    """
    Decorator to configure default parameters for the 'Go Hotel' application tests.
    These values serve as defaults for local runs (IDEs) but do not override 
    explicit environment variables.
    """
    cls.profile = "dev"
    cls.app_name = "go_hotel"
    cls.app_type = "web"
    cls.browser = "chrome"

    return cls
