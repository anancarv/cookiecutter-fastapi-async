import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import create_random_item, random_lower_string


@pytest.mark.asyncio
async def test_create_site(async_client: AsyncClient) -> None:
    data = {"name": random_lower_string(), "description": random_lower_string()}
    response = await async_client.post(
        "/items/",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content


@pytest.mark.asyncio
async def test_read_site(async_client: AsyncClient, db_session: AsyncSession) -> None:
    item = await create_random_item(db_session)
    response = await async_client.get(f"/items/{item.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item.name
    assert content["id"] == item.id
