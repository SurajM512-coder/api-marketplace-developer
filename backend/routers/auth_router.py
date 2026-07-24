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

from fastapi import Request
from fastapi.responses import RedirectResponse

from services.google_auth import oauth

from database.db import SessionLocal
from schemas.user_schema import UserRole

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
        "token_type": "bearer",
        "role": db_user.role
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



@router.get("/auth/google/login")
async def google_login(request: Request):

    redirect_uri = request.url_for("google_callback")

    print("Redirect URI:", redirect_uri)

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )



@router.get("/auth/google/callback")
async def google_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    email = user_info["email"]
    name = user_info["name"]

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            name=name,
            email=email,
            role=UserRole.consumer,
            email_verified=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return RedirectResponse(
       url=(
         f"http://localhost:5173/oauth-success"
           f"?token={access_token}"
           f"&role={user.role.value}"
        )
    )

