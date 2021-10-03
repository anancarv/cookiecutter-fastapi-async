import asyncio
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db import database

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
        await database.connect()
        # Try to create session to check if DB is awake
        await database.execute("SELECT 1")
        await database.disconnect()
    except Exception as error:
        logger.error(error)
        raise error
    logger.info("Service finished initializing")


if __name__ == "__main__":
    loop.run_until_complete(main())
