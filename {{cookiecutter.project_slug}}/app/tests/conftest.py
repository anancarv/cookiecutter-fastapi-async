import asyncio

import pytest
from httpx import AsyncClient

from app.db import database
from app.main import app


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://localhost:8080") as client:
        yield client


@pytest.yield_fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup():
    await database.connect()
    yield "Database connected"
    await database.disconnect()
    print("Database disconnected")
