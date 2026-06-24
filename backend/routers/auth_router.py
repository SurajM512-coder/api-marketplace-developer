from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User

from schemas.auth_schema import UserLogin

from fastapi.security import OAuth2PasswordRequestForm

from services.auth import (
    verify_password,
    create_access_token
)

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user by email
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    # Verify password
    if not verify_password(
        form_data.password,
        db_user.password
    ):
        return {
            "message": "Incorrect password"
        }

    if not db_user.email_verified:
        raise HTTPException(
           status_code=403,
           detail="Please verify your email first"
    )

    access_token = create_access_token(
         data={
             "sub": db_user.email
    }
)

    return {
        "access_token": access_token,
        "token_type": "bearer"
}



@router.get("/verify-email/{token}")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.verification_token == token
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )

    user.email_verified = True
    user.verification_token = None

    db.commit()

    return {
        "message": "Email verified successfully"
    }