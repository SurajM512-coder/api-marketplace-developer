from fastapi import APIRouter
from schemas.user_schema import UserRegister

router = APIRouter()

@router.post("/register")
def register_user(user: UserRegister):
    return {
        "message": "User registered",
        "user": user
    }