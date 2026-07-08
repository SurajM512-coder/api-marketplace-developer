from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):

    rating: int

    comment: Optional[str] = None



class ReviewUpdate(BaseModel):

    rating: Optional[int] = None

    comment: Optional[str] = None



class ReviewResponse(BaseModel):

    id: int

    user_id: int

    api_id: int

    rating: int

    comment: Optional[str]

    created_at: datetime


    class Config:
        from_attributes = True