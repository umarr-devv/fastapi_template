from pydantic import Field, BaseModel

from schemes.base import BaseScheme


class UserScheme(BaseScheme):
    username: str
    fullname: str


class CreateUserScheme(BaseModel):
    username: str = Field(min_length=4, max_length=64)
    fullname: str = Field(min_length=8, max_length=255)
    password: str = Field(min_length=6)


class LoginUserScheme(BaseModel):
    username: str = Field(min_length=4, max_length=64)
    password: str = Field(min_length=6)
