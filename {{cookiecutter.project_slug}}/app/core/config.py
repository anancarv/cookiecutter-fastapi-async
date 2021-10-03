import os


class Config:
    DATABASE_URL = (
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PWD']}@"
        f"db/{os.environ['POSTGRES_DB']}"
    )
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
