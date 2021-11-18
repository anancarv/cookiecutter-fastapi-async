from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Config

engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
