from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta    
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database.db import SessionLocal
from database.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)



def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )



def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    return verify_token(token)



def get_current_user_data(
    email: str = Depends(get_current_user)
):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



def require_developer(
    current_user: User = Depends(get_current_user_data)
):
    if current_user.role.value not in ["developer", "admin"]:
      raise HTTPException(
         status_code=403,
         detail="Developer access required"
    )

    return current_user



def require_admin(
    current_user: User = Depends(get_current_user_data)
):
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user