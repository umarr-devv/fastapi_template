from datetime import timedelta

import jwt
from src.utils.time_tools import utc_now


def create_token(
    data: dict, secret_key: str, expires_delta: timedelta, algorithm: str = 'HS256'
) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": utc_now() + expires_delta})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str, secret_key: str, algorithms: list[str] = ['HS256']) -> dict:
    return jwt.decode(token, secret_key, algorithms=algorithms)
