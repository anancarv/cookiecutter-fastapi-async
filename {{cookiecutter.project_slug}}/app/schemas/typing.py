from typing import TypeVar

from pydantic import BaseModel

from app.db import Base

ModelType = TypeVar("ModelType", bound=Base)
UpdateType = TypeVar("UpdateType", bound=BaseModel)
CreateType = TypeVar("CreateType", bound=BaseModel)
