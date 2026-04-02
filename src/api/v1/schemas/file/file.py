from api.v1.schemas.base import BaseSchema


class FileSchema(BaseSchema):
    file_name: str
    file_type: str
