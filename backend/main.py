from fastapi import FastAPI
from routers.user_router import router as user_router

from database.db import engine
from database.models import User, Base

from routers.auth_router import router as auth_router

from starlette.middleware.sessions import SessionMiddleware

from routers import api_router

from routers import api_key_router

from routers import subscription_router

from routers import usage_router

from routers import admin_router

from routers import review_router

from routers import dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="api_marketplace_google_oauth_secret"
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(api_router.router)
app.include_router(api_key_router.router)
app.include_router(subscription_router.router)
app.include_router(usage_router.router)
app.include_router(admin_router.router)
app.include_router(review_router.router)
app.include_router(
    dashboard_router.router
)

@app.get("/")
def home():
    return {"message": "API Marketplace Backend Running"}
    