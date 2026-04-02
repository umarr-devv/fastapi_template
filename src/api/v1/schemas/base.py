from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: str
    create_at: datetime
    update_at: datetime
