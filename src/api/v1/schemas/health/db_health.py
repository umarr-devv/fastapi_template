from pydantic import BaseModel


class DBHealthSchema(BaseModel):
    status: str
