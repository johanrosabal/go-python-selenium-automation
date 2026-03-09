class SingletonMeta(type):
    """
    A thread-safe implementation of the Singleton design pattern.

    Ensures that a class maintains only one active instance throughout the 
    application lifecycle. This is primarily used for Page Objects to 
    maintain state consistency and prevent redundant object instantiations.

    Attributes:
        _instances (dict): A thread-local storage mapping classes to their 
            corresponding unique instances.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Intercepts the class instantiation call (constructor).

        If an instance of the class already exists in the registry, it is 
        returned immediately. Otherwise, a new instance is created and cached.

        Returns:
            object: The unique instance of the calling class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def clear_instances(mcs):
        """
        Purges all cached Singleton instances from the registry.

        This method is critical between test iterations to ensure that 
        Page Objects are re-initialized with the current session's WebDriver context.
        """
        mcs._instances = {}
