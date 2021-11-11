from typing import TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
UpdateType = TypeVar("UpdateType", bound=BaseModel)
CreateType = TypeVar("CreateType", bound=BaseModel)
