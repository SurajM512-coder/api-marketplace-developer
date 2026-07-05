from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey

from datetime import datetime

from database.db import Base

from sqlalchemy import Enum as SQLEnum

from schemas.user_schema import UserRole

from sqlalchemy.orm import relationship


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




class API(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    base_url = Column(String, nullable=False)

    category = Column(String, nullable=False)

    version = Column(String, default="1.0.0")

    pricing = Column(String, default="Free")

    developer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
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

    developer = relationship(
        "User",
        backref="apis"
    )




class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    key = Column(
        String,
        unique=True,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    api_id = Column(
        Integer,
        ForeignKey("apis.id"),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    user = relationship(
        "User",
        backref="api_keys"
    )


    api = relationship(
        "API",
        backref="api_keys"
    )