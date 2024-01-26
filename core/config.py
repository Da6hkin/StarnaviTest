import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    db_echo: bool = False
    jwt_secret: str = os.getenv("PRIVATE_KEY")
    jwt_algo: str = "HS256"
    jwt_expire: int = 60


settings = Settings()
