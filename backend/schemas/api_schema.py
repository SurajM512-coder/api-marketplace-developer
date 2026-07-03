from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class APICreate(BaseModel):
    name: str
    description: str
    base_url: str
    category: str
    version: Optional[str] = "1.0.0"
    pricing: Optional[str] = "Free"


class APIUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_url: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None
    pricing: Optional[str] = None


class APIResponse(BaseModel):
    id: int
    name: str
    description: str
    base_url: str
    category: str
    version: str
    pricing: str
    developer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True