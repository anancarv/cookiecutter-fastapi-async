import random
import string

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def create_random_item(database: AsyncSession) -> models.Item:
    name = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(name=name, description=description)
    return await crud.item.create(database, item_in)
