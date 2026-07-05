from pydantic import BaseModel
from datetime import datetime


class APIKeyResponse(BaseModel):
    id: int
    key: str
    user_id: int
    api_id: int
    is_active: bool
    created_at: datetime


    class Config:
        from_attributes = True