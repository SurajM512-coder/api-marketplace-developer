from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from database.db import get_db

from database.models import (
    User,
    API,
    Subscription,
    APIUsage
)


from services.auth import get_current_user_data



router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)



@router.get("/analytics")
def admin_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


    total_users = db.query(User).count()


    total_apis = db.query(API).count()


    total_subscriptions = db.query(
        Subscription
    ).count()


    total_requests = db.query(
        APIUsage
    ).count()


    return {
        "total_users": total_users,
        "total_apis": total_apis,
        "total_subscriptions": total_subscriptions,
        "total_api_requests": total_requests
    }