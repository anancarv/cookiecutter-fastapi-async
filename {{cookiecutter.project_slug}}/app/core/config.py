import os


class Config:
    DATABASE_URL = (
        f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:"
        f"{os.environ['POSTGRES_PASSWORD']}@db/{os.environ['POSTGRES_DB']}"
    )
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
