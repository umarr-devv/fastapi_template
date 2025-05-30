from aiocache import caches
from pydantic import BaseModel

from core.config import config


class RedisCacheConfig(BaseModel):
    cache: str = 'aiocache.RedisCache'
    endpoint: str = config.redis.host
    port: int = 6379
    timeout: int = 3
    serializer: dict[str, str] = {
        'class': 'aiocache.serializers.PickleSerializer'
    }
    plugins: list[dict[str, str]] = [
        {"class": "aiocache.plugins.HitMissRatioPlugin"},
        {"class": "aiocache.plugins.TimingPlugin"},
    ]

    @classmethod
    def set(cls):
        instance = cls()
        caches.set_config({
            'default': instance.model_dump()
        })
