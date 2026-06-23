from fastapi import FastAPI
from routers.user_router import router as user_router

from database.db import engine
from database.models import User, Base

from routers.auth_router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "API Marketplace Backend Running"}
    