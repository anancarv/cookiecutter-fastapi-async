from pydantic import BaseModel

from .item import Item, ItemCreate, ItemUpdate


class Message(BaseModel):
    detail: str


__all__ = ["Message", "Item", "ItemCreate", "ItemUpdate"]
