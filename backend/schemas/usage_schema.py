from pydantic import BaseModel
from datetime import datetime


class UsageResponse(BaseModel):

    id: int

    api_id: int

    user_id: int

    api_key_id: int

    endpoint: str

    method: str

    timestamp: datetime


    class Config:
        from_attributes = True