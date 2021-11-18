import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.db import async_session, engine
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def db_session():
    async with engine.begin() as connection:
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_db(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def main_app(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
async def async_client(main_app):
    async with AsyncClient(app=main_app, base_url="http://localhost:8080") as client:
        yield client
