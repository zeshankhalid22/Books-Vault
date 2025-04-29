import logging
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.core.config import settings

# Initialize logger
logger = logging.getLogger(__name__)

class DatabaseEngineFactory:
    """Factory to create a database engine with appropriate settings based on the database type."""

    @staticmethod
    def get_engine(database_url: str) -> AsyncEngine:
        """Creates and returns an asynchronous database engine based on the database URL."""
        if database_url.startswith("sqlite"):
            return DatabaseEngineFactory._create_sqlite_engine()
        elif database_url.startswith("postgres"):
            return DatabaseEngineFactory._create_postgres_engine()
        else:
            logger.error(f"Unsupported database URL: {database_url}")
            raise NotImplementedError(f"Unsupported database URL: {database_url}")

    @staticmethod
    def _create_sqlite_engine() -> AsyncEngine:
        """Create an SQLite database engine."""
        logger.info("Creating SQLite engine.")
        return create_async_engine(
            url=settings.SQLITE_URI,
            echo=settings.SQLLITE_ECHO,  # Configurable SQL logging
            connect_args={"check_same_thread": False},  # Required for async SQLite
        )

    @staticmethod
    def _create_postgres_engine() -> AsyncEngine:
        """Create a PostgreSQL database engine with connection pooling."""
        logger.info("Creating PostgreSQL engine.")
        return create_async_engine(
            url=settings.POSTGRES_URL,
            echo=settings.POSTGRES_ECHO,  # Configurable SQL logging
            pool_recycle=1800,  # Recycle connections every 30 minutes
            pool_size=15,  # Number of connections to keep open
            max_overflow=5,  # Allow 5 additional temporary connections
            pool_timeout=30,  # Wait up to 30 seconds for a connection
        )


# Create the engine dynamically based on the database URL
engine = DatabaseEngineFactory.get_engine(settings.POSTGRES_URL if settings.POSTGRES_URL else settings.SQLITE_URI)