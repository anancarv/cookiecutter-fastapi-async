from typing import List

from databases.core import Database
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as
from sqlalchemy import Table

from app import models, schemas
from app.exception import ItemNotFoundException


class Item:
    def __init__(self, item_table: Table):
        self.item_table = item_table

    async def create(
        self, database: Database, item_obj: schemas.ItemCreate
    ) -> schemas.Item:
        query_insert = self.item_table.insert()
        obj_id = await database.execute(query_insert, jsonable_encoder(item_obj))
        return await self.get(database, obj_id)

    async def get(self, database: Database, item_id: int) -> schemas.Item:
        query = self.item_table.select().where(self.item_table.c.id == item_id)
        found_item = await database.fetch_one(query)

        if found_item is None:
            raise ItemNotFoundException("Item not found")

        return parse_obj_as(schemas.Item, jsonable_encoder(found_item))

    async def list(self, database: Database) -> List[schemas.Item]:
        query = self.item_table.select()
        all_items = await database.fetch_all(query)
        return parse_obj_as(List[schemas.Item], jsonable_encoder(all_items))

    async def update(
        self, database: Database, item_obj: schemas.Item, item_in: schemas.ItemUpdate
    ) -> schemas.Item:

        obj_data = jsonable_encoder(item_obj)
        if isinstance(item_in, dict):
            update_data = item_in
        else:
            update_data = item_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(item_obj, field, update_data[field])

        query = (
            self.item_table.update()
            .where(self.item_table.c.id == item_obj.id)
            .values(jsonable_encoder(item_obj))
        )
        await database.execute(query)
        return item_obj

    async def delete(self, database: Database, item_id: int) -> None:
        await self.get(database, item_id)
        query = self.item_table.delete().where(self.item_table.c.id == item_id)
        await database.execute(query)


item = Item(models.Item.__table__)  # pylint: disable=no-member
