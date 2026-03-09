import yaml
import os
from pathlib import Path

class ConfigManager:
    """
    Utility class to load and manage environment-specific configurations from YAML files.
    """
    _config = None
    _env = None

    @classmethod
    def load_config(cls, app_path: str, env: str = None):
        """
        Loads the YAML configuration for the specified environment.
        
        Args:
            app_path (str): The absolute or relative path to the application directory 
                            (e.g., 'applications/web/demo').
            env (str, optional): The environment name (qa, dev, uat, prod). 
                                 If None, it tries to read from the 'ENV' environment variable.
                                 Defaults to 'qa' if neither is provided.
        """
        if env:
            cls._env = env.lower()
        else:
            cls._env = os.getenv('ENV', 'qa').lower()

        config_path = Path(app_path) / "config" / "environments" / f"{cls._env}.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found for environment '{cls._env}' at: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as file:
            cls._config = yaml.safe_load(file)
        
        return cls._config

    @classmethod
    def get(cls, key: str, default=None):
        """
        Retrieves a configuration value by key. Supports nested keys with dot notation (e.g., 'web.base_url').
        """
        if cls._config is None:
            raise ValueError("Configuration not loaded. Call ConfigManager.load_config() first.")

        keys = key.split('.')
        value = cls._config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    @classmethod
    def get_env(cls):
        """Returns the current active environment name."""
        return cls._env
