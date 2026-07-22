from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User

from services.auth import hash_password

import secrets

from schemas.user_schema import (

    UserRegister,

    UserResponse,

    UserUpdate,

    UserRole

)

from services.email_service import send_verification_email

from services.auth import (
    get_current_user,
    require_developer,
    require_admin
)
from fastapi import Depends


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

     raise HTTPException(
        status_code=400,
        detail="Email already registered"
    )
    
    if user.role == UserRole.admin:
      raise HTTPException(
          status_code=403,
          detail="Admin accounts cannot be created through public registration"
        )

    token = secrets.token_urlsafe(32)

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        email_verified=False,
        verification_token=token
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)
    
    send_verification_email(
        new_user.email,
        new_user.verification_token
)

    return {
        "message": "User registered"
    }



@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(User).all()



@router.get(
    "/users/{id}",
    response_model=UserResponse
)
def get_user(
    id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == id
    ).first()

    if not user:

     raise HTTPException(
        status_code=404,
        detail="User not found"
    )

    return user



@router.put(
    "/users/{id}",
    response_model=UserResponse
)
def update_user(
    id: int,
    updated_user: UserUpdate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check if another user already uses this email
    if updated_user.email is not None:

        existing_user = db.query(User).filter(
            User.email == updated_user.email,
            User.id != id
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        user.email = updated_user.email

    # Update only provided fields
    if updated_user.name is not None:
        user.name = updated_user.name

    if updated_user.password is not None:
        user.password = hash_password(
            updated_user.password
        )

    if updated_user.role is not None:
        user.role = updated_user.role

    db.commit()
    db.refresh(user)

    return user



@router.delete("/users/{id}")

def delete_user(

    id: int,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(

        User.id == id

    ).first()


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    db.delete(user)

    db.commit()


    return {

        "message": "User deleted successfully"

    }



@router.get("/developer-test")
def developer_test(
    current_user = Depends(require_developer)
):
    return {
        "message": f"Welcome Developer {current_user.name}"
    }



@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_admin)
):
    return {
        "message": f"Welcome Admin {current_user.name}"
    }