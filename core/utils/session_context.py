class SessionContext:
    """
    Singleton utility to share and store data across different test cases 
    within the same execution session.
    """
    _storage = {}

    @classmethod
    def set(cls, key: str, value):
        """Stores a value in the session context."""
        cls._storage[key] = value

    @classmethod
    def get(cls, key: str, default=None):
        """Retrieves a value from the session context."""
        return cls._storage.get(key, default)

    @classmethod
    def clear(cls):
        """Clears all stored data."""
        cls._storage.clear()
