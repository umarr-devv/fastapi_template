from pydantic import BaseModel, Field


class PatchUserSchema(BaseModel):
    username: str | None = Field(max_length=64, min_length=4, default=None)
    fullname: str | None = Field(max_length=256, default=None)


class PatchUserPasswordSchema(BaseModel):
    password: str = Field(min_length=8, max_length=256)
