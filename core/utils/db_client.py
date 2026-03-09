from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from core.utils.logger_config import setup_logger
from core.utils.config_manager import ConfigManager

class DBClient:
    """
    Generic Database Client using SQLAlchemy.
    Supports multiple dialects (PostgreSQL, MySQL, SQL Server, etc.)
    """
    def __init__(self, connection_key: str = "database.url"):
        self.logger = setup_logger(f"DBClient[{connection_key}]")
        self.connection_url = ConfigManager.get(connection_key)
        
        if not self.connection_url:
            self.logger.warning(f"No connection URL found for key: {connection_key}")
            self.engine = None
            self._session_factory = None
            return

        try:
            # Create Engine
            self.engine = create_engine(
                self.connection_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )
            # Create Session Factory
            self._session_factory = scoped_session(
                sessionmaker(bind=self.engine)
            )
            self.logger.info(f"Database engine initialized for: {connection_key}")
        except Exception as e:
            self.logger.error(f"Failed to initialize database engine: {e}")
            self.engine = None
            self._session_factory = None

    def execute_query(self, query: str, params: dict = None):
        """Executes a SQL query and returns the result."""
        if not self.engine:
            raise RuntimeError("Database engine not initialized.")

        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            if result.returns_rows:
                return [dict(row._mapping) for row in result]
            connection.commit()
            return None

    def get_session(self):
        """Returns a new database session."""
        if not self._session_factory:
            raise RuntimeError("Database session factory not initialized.")
        return self._session_factory()

    def close_all(self):
        """Closes all connections in the pool."""
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connections closed.")
