import os

import dotenv
import pydantic

ENV_PATH = os.getcwd().join('.env')
dotenv.load_dotenv()


class DataBaseConfig(pydantic.BaseModel):
    database: str
    host: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"


class Config(pydantic.BaseModel):
    db: DataBaseConfig


config = Config(
    db=DataBaseConfig(
        database=os.getenv('pg_database'),
        host=os.getenv('pg_host'),
        user=os.getenv('pg_user'),
        password=os.getenv('pg_password'),
    )
)
