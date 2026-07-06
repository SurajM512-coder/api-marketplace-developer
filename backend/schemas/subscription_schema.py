from pydantic import BaseModel
from datetime import datetime


class SubscriptionResponse(BaseModel):

    id: int

    user_id: int

    api_id: int

    is_active: bool

    subscribed_at: datetime


    class Config:
        from_attributes = True