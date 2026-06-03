def project_config(app_name: str, app_class: type, app_type: str = "web"):
    """
    Class decorator to inject project-specific configuration into a BaseTest class.
    
    Args:
        app_name (str): The name of the project (e.g., 'pc_agency_portal').
        app_class (type): The App Orchestrator class to instantiate.
        app_type (str, optional): The application type, defaults to 'web'.
    """
    def decorator(cls):
        cls.app_name = app_name
        cls.app_class = app_class
        cls.app_type = app_type
        return cls
    return decorator
