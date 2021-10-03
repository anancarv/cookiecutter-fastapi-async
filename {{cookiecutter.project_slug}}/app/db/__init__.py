import databases
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from app.core.config import Config

Base: DeclarativeMeta = declarative_base()
database: databases.core.Database = databases.Database(Config.DATABASE_URL)
