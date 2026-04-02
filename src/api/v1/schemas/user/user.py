from api.v1.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    username: str
    fullname: str
