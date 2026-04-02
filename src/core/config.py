import os

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AppConfig(ConfigBase):
    secret_key: str

    model_config = SettingsConfigDict(env_prefix="app_")


class DataBaseConfig(ConfigBase):
    host: str
    database: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"

    model_config = SettingsConfigDict(env_prefix="pg_")


class LoggingConfig(ConfigBase):
    level: str
    format: str
    interval: int
    when: str

    model_config = SettingsConfigDict(env_prefix="log_")


class JWTConfig(ConfigBase):
    private_key: str

    model_config = SettingsConfigDict(env_prefix="jwt_")


class RedisConfig(ConfigBase):
    host: str
    port: int
    model_config = SettingsConfigDict(env_prefix="redis_")


class SuperAdminConfig(ConfigBase):
    username: str
    password: str

    model_config = SettingsConfigDict(env_prefix="admin_")


class ConfigModel(BaseModel):
    app: AppConfig = Field(default_factory=AppConfig)  # type: ignore
    database: DataBaseConfig = Field(default_factory=DataBaseConfig)  # type: ignore
    logging: LoggingConfig = Field(default_factory=LoggingConfig)  # type: ignore
    jwt: JWTConfig = Field(default_factory=JWTConfig)  # type: ignore
    redis: RedisConfig = Field(default_factory=RedisConfig)  # type: ignore
    admin: SuperAdminConfig = Field(default_factory=SuperAdminConfig)  # type: ignore

    @classmethod
    def load(cls) -> "ConfigModel":
        return cls()


config = ConfigModel.load()
