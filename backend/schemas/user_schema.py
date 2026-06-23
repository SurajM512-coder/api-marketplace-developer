from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):

    id: int

    name: str

    email: str

    class Config:

        from_attributes = True

class UserUpdate(BaseModel):

    name: str

    email: EmailStr

    password: str