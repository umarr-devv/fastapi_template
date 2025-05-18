from pydantic import BaseModel


class TokenPayloadScheme(BaseModel):
    sub: str
    username: str


class TokenScheme(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
