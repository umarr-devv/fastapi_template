from pydantic import BaseModel


class TokenPayloadSchema(BaseModel):
    sub: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"
