from sqlalchemy import Column, Integer, String, Boolean, DateTime

from datetime import datetime

from database.db import Base

from sqlalchemy import Enum as SQLEnum

from schemas.user_schema import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True)

    password = Column(String)

    role = Column(
        SQLEnum(UserRole),
        default=UserRole.consumer
)

    email_verified = Column(
        Boolean,
        default=False
    )

    
    verification_token = Column(
        String,
        nullable=True,
        unique=True
)

    otp = Column(
        String,
        nullable=True
    )   

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )