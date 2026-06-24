from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User

from schemas.auth_schema import UserLogin

from services.auth import verify_password

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    # Verify password
    if not verify_password(
        user.password,
        db_user.password
    ):
        return {
            "message": "Incorrect password"
        }

    return {
        "message": "Login successful"
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