from datetime import timedelta, datetime, timezone

import jwt

from core.config import config


class JWTService:
    algorithm = 'HS256'

    @staticmethod
    def encode(
            payload: dict,
            expires_delta: timedelta = timedelta(days=28),
    ) -> str:
        to_encode = payload.copy()
        to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
        return jwt.encode(to_encode, key=config.jwt.private_key, algorithm=JWTService.algorithm)

    @staticmethod
    def decode(data: str) -> dict:
        return jwt.decode(data, key=config.jwt.private_key, algorithms=[JWTService.algorithm])
