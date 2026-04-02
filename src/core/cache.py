from aiocache import caches
from pydantic import BaseModel

from core.config import config


class MemoryCacheConfig(BaseModel):
    cache: str = "aiocache.SimpleMemoryCache"
    serializer: dict[str, str] = {"class": "aiocache.serializers.StringSerializer"}


class RedisCacheConfig(BaseModel):
    cache: str = "aiocache.RedisCache"
    endpoint: str = config.redis.host
    port: int = config.redis.port
    timeout: int = 3
    serializer: dict[str, str] = {"class": "aiocache.serializers.PickleSerializer"}
    plugins: list[dict[str, str]] = [
        {"class": "aiocache.plugins.HitMissRatioPlugin"},
        {"class": "aiocache.plugins.TimingPlugin"},
    ]


class CacheConfig(BaseModel):

    default: MemoryCacheConfig = MemoryCacheConfig()
    redis: RedisCacheConfig = RedisCacheConfig()

    @classmethod
    def set(cls):
        instance = cls()
        caches.set_config(instance.model_dump())
