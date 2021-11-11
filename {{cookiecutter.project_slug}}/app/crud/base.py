import logging
from typing import Generic, List, Optional, get_args

from databases.core import Database
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as
from sqlalchemy import Table, and_
from sqlalchemy.sql.elements import ClauseElement

from app import schemas
from app.exceptions import ModelNotFoundException

logger = logging.getLogger(__name__)


class CRUDBase(Generic[schemas.ModelType, schemas.CreateType, schemas.UpdateType]):
    def __init__(self, table: Table):
        self._table = table
        (self._model_type, self._create_type, self._update_type) = get_args(
            self.__orig_bases__[0]  # type: ignore
        )

    @property
    def table(self) -> Table:
        return self._table

    async def create(
        self, database: Database, obj: schemas.CreateType
    ) -> schemas.ModelType:
        query_insert = self._table.insert()
        obj_id = await database.execute(query_insert, jsonable_encoder(obj))
        logger.debug(f"{obj} successfully created")

        return await self.get(database, obj_id)

    async def get(self, database: Database, obj_id: int) -> schemas.ModelType:
        query = self._table.select().where(self._table.c.id == obj_id)
        found_obj = await database.fetch_one(query)

        model_name = self._model_type.__name__
        if found_obj is None:
            logger.error(f"{model_name} id={obj_id} not found")
            error = schemas.ErrorModel(model_name=model_name, value=obj_id)
            raise ModelNotFoundException(error)

        logger.debug(f"{model_name} id={obj_id} found")
        return parse_obj_as(self._model_type, jsonable_encoder(found_obj))

    async def list(
        self,
        database: Database,
        clauses: Optional[List[ClauseElement]] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[schemas.ModelType]:

        if clauses is None:
            clauses = []

        query = self._table.select().where(and_(*clauses)).offset(offset).limit(limit)
        results = await database.fetch_all(query)
        logger.debug(f"List all {self._model_type.__name__} successful")

        return [self._model_type(**obj) for obj in jsonable_encoder(results)]

    async def count(self, database: Database) -> int:
        return int(await database.execute(self._table.count()))

    async def update(
        self, database: Database, obj_in: schemas.UpdateType, obj_id: int
    ) -> schemas.ModelType:

        found_db_obj = await self.get(database, obj_id)
        db_obj = parse_obj_as(self._model_type, jsonable_encoder(found_db_obj))

        update_data = obj_in.dict(exclude_unset=True)
        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        obj_id = db_obj.id
        query = (
            self._table.update()
            .where(self._table.c.id == obj_id)
            .values(jsonable_encoder(db_obj))
        )
        await database.execute(query)
        logger.debug(f"{self._model_type.__name__} id={obj_id} successfully updated")
        return db_obj

    async def delete(self, database: Database, obj_id: int) -> None:
        await self.get(database, obj_id)
        query = self._table.delete().where(self._table.c.id == obj_id)
        await database.execute(query)
        logger.debug(f"{self._model_type.__name__} successfully deleted")

    async def bulk_delete(
        self, database: Database, clauses: List[ClauseElement]
    ) -> None:
        query = self._table.delete().where(and_(*clauses))
        await database.execute(query)
        logger.debug(f"{self._model_type.__name__} bulk successfully deleted")
