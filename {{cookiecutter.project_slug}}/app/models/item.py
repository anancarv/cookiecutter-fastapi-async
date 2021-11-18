from sqlalchemy import Column, Integer, String

from app.db import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
