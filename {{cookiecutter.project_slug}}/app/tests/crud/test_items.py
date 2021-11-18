import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.exceptions import ModelNotFoundException
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils import random_lower_string


@pytest.mark.asyncio
async def test_create_item_success(db_session: AsyncSession) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    item = await crud.item.create(db_session, item_in)
    assert item.name == name
    assert item.description == description
    assert item.id
    assert isinstance(item.id, int)


@pytest.mark.asyncio
async def test_create_item_fail_item_already_exist(db_session: AsyncSession) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    item = await crud.item.create(db_session, item_in)

    with pytest.raises(IntegrityError):
        item2 = await crud.item.create(db_session, item_in)
        stored_item = await crud.item.get(db_session, item.id)

        assert stored_item
        assert item2 is None


@pytest.mark.asyncio
async def test_get_item_success(db_session: AsyncSession) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    item = await crud.item.create(db_session, item_in)
    stored_item = await crud.item.get(db_session, item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.name == stored_item.name


@pytest.mark.asyncio
async def test_get_item_fail_item_not_found(db_session: AsyncSession) -> None:
    item_id = 150

    with pytest.raises(ModelNotFoundException):
        stored_item = await crud.item.get(db_session, item_id)

        assert stored_item is None


@pytest.mark.asyncio
async def test_update_item_success(db_session: AsyncSession) -> None:
    name = random_lower_string()
    description = random_lower_string()

    item_in = ItemCreate(name=name, description=description)
    item = await crud.item.create(db_session, item_in)
    item_name = item.name

    new_name = random_lower_string()
    item_in_2 = ItemUpdate(name=new_name)
    updated_item = await crud.item.update(db_session, item_in_2, item.id)

    assert updated_item
    assert item.id == updated_item.id
    assert item_name != updated_item.name
    assert updated_item.description == description
    assert updated_item.name == new_name


@pytest.mark.asyncio
async def test_delete_item(db_session: AsyncSession) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    item = await crud.item.create(db_session, item_in)

    await crud.item.delete(db_session, item.id)

    with pytest.raises(ModelNotFoundException):
        item2 = await crud.item.get(db_session, item.id)
        assert item2 is None
