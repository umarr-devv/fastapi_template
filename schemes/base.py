from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseScheme(BaseModel):
    id: str
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)
