from pydantic import BaseModel, Field


class LoginUserSchema(BaseModel):
    username: str = Field(max_length=64, min_length=4)
    password: str = Field(max_length=256, min_length=8)
