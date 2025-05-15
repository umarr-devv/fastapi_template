import os

import dotenv
from pydantic import BaseModel

ENV_PATH = os.getcwd().join('.env')
dotenv.load_dotenv()


class ConfigModel(BaseModel):
    pg_host: str
    pg_database: str
    pg_user: str
    pg_password: str
    jwt_private_key: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}/{self.pg_database}"


config = ConfigModel(
    pg_host=os.getenv('pg_host'),
    pg_database=os.getenv('pg_database'),
    pg_user=os.getenv('pg_user'),
    pg_password=os.getenv('pg_password'),
    jwt_private_key=os.getenv('jwt_private_key'),
)
