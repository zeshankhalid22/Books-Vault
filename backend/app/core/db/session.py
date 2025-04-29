from collections.abc import AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.db.engine import engine

# Create an async session factory
async_session_maker = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Initialize logger
logger = logging.getLogger(__name__)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides an async database session and ensures proper lifecycle management."""
    async with async_session_maker() as session:
        logger.debug("Async database session created.")
        try:
            yield session
        except Exception as e:
            logger.error(f"Error during database session: {type(e).__name__}: {str(e)}")
            raise  # Re-raise exceptions for proper error handling
        finally:
            logger.debug("Async database session closed.")