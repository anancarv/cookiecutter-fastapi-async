from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Shared properties"""

    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Properties to receive on item creation"""


class ItemUpdate(ItemBase):
    """Properties to receive on item update"""


class ItemInDBBase(ItemBase):
    """ " Properties shared by models stored in DB"""

    id: int

    class Config:
        orm_mode = True


class Item(ItemInDBBase):
    """Properties to return to client"""


class ItemInDB(ItemInDBBase):
    """ " Properties properties stored in DB"""
