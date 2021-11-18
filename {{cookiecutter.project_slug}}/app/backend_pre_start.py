import asyncio
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db import async_session

logger = logging.getLogger(__name__)

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1

loop = asyncio.get_event_loop()


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def main() -> None:
    logger.info("Initializing service")
    try:
        async with async_session() as session:
            await session.execute("SELECT 1")
    except Exception as error:
        logger.error(error)
        raise error
    logger.info("Service finished initializing")


if __name__ == "__main__":
    loop.run_until_complete(main())
