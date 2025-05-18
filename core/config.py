import os

import dotenv
from pydantic import BaseModel

ENV_PATH = os.getcwd().join('.env-docker')
dotenv.load_dotenv()


class ConfigModel(BaseModel):
    pg_host: str
    pg_database: str
    pg_user: str
    pg_password: str
    log_level: str
    jwt_private_key: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}/{self.pg_database}"


config = ConfigModel(
    pg_host=os.getenv('PG_HOST'),
    pg_database=os.getenv('PG_DATABASE'),
    pg_user=os.getenv('PG_USER'),
    pg_password=os.getenv('PG_PASSWORD'),
    log_level=os.getenv('LOG_LEVEL'),
    jwt_private_key=os.getenv('JWT_PRIVATE_KEY'),
)
