from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User

from services.auth import hash_password

from schemas.user_schema import (

    UserRegister,

    UserResponse,

    UserUpdate

)


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

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered"
    }



@router.get(
    "/users",

    response_model=list[UserResponse]
)

def get_users(

    db: Session = Depends(get_db)

):

    users = db.query(User).all()

    return users



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

    existing_user = db.query(User).filter(

    User.email == updated_user.email,

    User.id != id

    ).first()


    if existing_user:

     raise HTTPException(

        status_code=400,

        detail="Email already registered"

    )


    user.name = updated_user.name

    user.email = updated_user.email

    user.password = hash_password(
        updated_user.password
    )


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