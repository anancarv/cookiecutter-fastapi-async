from typing import Any

from pydantic import BaseModel

from .item import Item, ItemCreate, ItemUpdate
from .typing import CreateType, ModelType, UpdateType


class Message(BaseModel):
    detail: str


class ErrorModel(BaseModel):
    class_name: str
    value: Any


__all__ = [
    "Message",
    "Item",
    "ItemCreate",
    "ItemUpdate",
    "CreateType",
    "ModelType",
    "UpdateType",
]
