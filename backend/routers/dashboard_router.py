from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)


from sqlalchemy.orm import Session

from sqlalchemy import func


from database.db import get_db


from database.models import (
    User,
    API,
    Subscription,
    APIUsage,
    APIKey
)


from services.auth import get_current_user_data



router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)




@router.get(
    "/developer"
)
def developer_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    developer_apis = db.query(API).filter(
        API.developer_id == current_user.id
    ).all()



    total_apis = len(
        developer_apis
    )


    api_ids = [
        api.id
        for api in developer_apis
    ]



    total_subscribers = db.query(
        Subscription
    ).filter(
        Subscription.api_id.in_(
            api_ids
        ),
        Subscription.is_active == True
    ).count()



    total_requests = db.query(
        APIUsage
    ).filter(
        APIUsage.api_id.in_(
            api_ids
        )
    ).count()



    top_api = (
        db.query(
            API.name,
            func.count(APIUsage.id).label(
                "requests"
            )
        )
        .join(
            APIUsage,
            API.id == APIUsage.api_id
        )
        .filter(
            API.developer_id == current_user.id
        )
        .group_by(
            API.id
        )
        .order_by(
            func.count(APIUsage.id).desc()
        )
        .first()
    )



    return {
        "total_apis": total_apis,

        "total_subscribers": total_subscribers,

        "total_requests": total_requests,

        "top_api": {
            "name": top_api.name,
            "requests": top_api.requests
        } if top_api else None
    }




@router.get(
    "/consumer"
)
def consumer_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    active_subscriptions = db.query(
        Subscription
    ).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True
    ).count()



    total_api_keys = db.query(
        APIKey
    ).filter(
        APIKey.user_id == current_user.id
    ).count()



    total_requests = db.query(
        APIUsage
    ).filter(
        APIUsage.user_id == current_user.id
    ).count()



    recent_usage = (
        db.query(
            APIUsage
        )
        .filter(
            APIUsage.user_id == current_user.id
        )
        .order_by(
            APIUsage.timestamp.desc()
        )
        .limit(5)
        .all()
    )



    return {
        "active_subscriptions": active_subscriptions,

        "total_api_keys": total_api_keys,

        "total_requests": total_requests,

        "recent_activity": [
            {
                "api_id": usage.api_id,
                "endpoint": usage.endpoint,
                "method": usage.method,
                "timestamp": usage.timestamp
            }

            for usage in recent_usage
        ]
    }




@router.get(
    "/admin"
)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can access dashboard"
        )



    total_users = db.query(
        User
    ).count()



    total_apis = db.query(
        API
    ).count()



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

        "total_requests": total_requests
    }