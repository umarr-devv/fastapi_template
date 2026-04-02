from datetime import datetime

from pydantic import BaseModel


class CacheHealthSchema(BaseModel):
    date: datetime
