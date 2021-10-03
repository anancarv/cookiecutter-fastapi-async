import random
import string

from databases.core import Database

from app import crud
from app.schemas import Item, ItemCreate


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def create_random_item(database: Database) -> Item:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    return await crud.item.create(database, item_in)
