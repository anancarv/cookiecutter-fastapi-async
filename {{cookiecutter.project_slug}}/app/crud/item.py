from app import models, schemas
from app.crud.base import CRUDBase


class CRUDItem(CRUDBase[schemas.Item, schemas.ItemCreate, schemas.ItemUpdate]):
    pass


item = CRUDItem(models.Item.__table__)
