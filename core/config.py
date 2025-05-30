from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DataBaseConfig(ConfigBase):
    host: str
    database: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"

    model_config = SettingsConfigDict(
        env_prefix='pg_'
    )


class LoggingConfig(ConfigBase):
    level: str
    format: str
    interval: int
    when: str

    model_config = SettingsConfigDict(
        env_prefix='log_'
    )


class JWTConfig(ConfigBase):
    private_key: str

    model_config = SettingsConfigDict(
        env_prefix='jwt_'
    )


class RedisConfig(ConfigBase):
    host: str

    model_config = SettingsConfigDict(
        env_prefix='redis_'
    )


class ConfigModel(BaseModel):
    database: DataBaseConfig = Field(default_factory=DataBaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)

    @classmethod
    def load(cls) -> 'ConfigModel':
        return cls()


config = ConfigModel.load()
