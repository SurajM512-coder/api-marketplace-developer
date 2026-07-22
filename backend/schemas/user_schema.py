from pydantic import BaseModel, EmailStr, field_validator
import re

from datetime import datetime

from enum import Enum

from typing import Optional

class UserRole(str, Enum):
    consumer = "consumer"
    developer = "developer"
    admin = "admin"


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.consumer

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):

        if len(password) < 8:
            raise ValueError(
                "Password must be at least 8 characters long"
            )

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(r"\d", password):
            raise ValueError(
                "Password must contain at least one number"
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return password



class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    email_verified: bool
    verification_token: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None

    password: Optional[str] = None

    role: Optional[UserRole] = None
