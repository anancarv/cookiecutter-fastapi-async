from sqlalchemy import Column, Integer, String

from app.db import Base


class Item(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
