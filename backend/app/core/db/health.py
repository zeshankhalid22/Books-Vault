import logging
from sqlalchemy.sql import text
from app.core.db.engine import engine

# Initialize logger
logger = logging.getLogger(__name__)

async def check_db_ready() -> None:
    """Checks if the database is ready for operations. Verifies connectivity using a lightweight query."""
    try:
        async with engine.begin() as conn:
            logger.debug("Checking database connectivity.")
            result = await conn.execute(text("SELECT 1"))
            _ = result.scalar()
            logger.info("Database connectivity check passed.")
    except Exception as e:
        logger.error(f"Database connectivity check failed: {type(e).__name__}: {str(e)}")
        raise