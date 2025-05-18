from pydantic import BaseModel


class HealthScheme(BaseModel):
    status: str
