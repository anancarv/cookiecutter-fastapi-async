import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session

logger = logging.getLogger(__name__)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            logger.error("Transaction failed, rolling back")
            await session.rollback()
            raise
