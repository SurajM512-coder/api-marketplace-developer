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
    APIUsage,
    Review
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




@router.get(
    "/users"
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    users = db.query(
        User
    ).all()



    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

        for user in users
    ]




@router.put(
    "/users/{user_id}/role"
)
def change_user_role(
    user_id: int,
    new_role: str,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()



    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )



    allowed_roles = [
        "consumer",
        "developer",
        "admin"
    ]



    if new_role not in allowed_roles:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )



    user.role = new_role



    db.commit()

    db.refresh(
        user
    )



    return {
        "message": "User role updated successfully",

        "user": {
            "id": user.id,
            "name": user.name,
            "role": user.role
        }
    }




@router.put(
    "/users/{user_id}/disable"
)
def disable_user(
    user_id: int,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()



    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )



    user.is_active = False



    db.commit()

    db.refresh(
        user
    )



    return {
        "message": "User disabled successfully",

        "user": {
            "id": user.id,
            "name": user.name,
            "active": user.is_active
        }
    }




@router.put(
    "/users/{user_id}/enable"
)
def enable_user(
    user_id: int,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()



    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )



    user.is_active = True



    db.commit()

    db.refresh(
        user
    )



    return {
        "message": "User enabled successfully",

        "user": {
            "id": user.id,
            "name": user.name,
            "active": user.is_active
        }
    }




@router.put(
    "/apis/{api_id}/approve"
)
def approve_api(
    api_id: int,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    api = db.query(
        API
    ).filter(
        API.id == api_id
    ).first()



    if not api:

        raise HTTPException(
            status_code=404,
            detail="API not found"
        )



    api.status = "approved"



    db.commit()

    db.refresh(
        api
    )



    return {
        "message": "API approved successfully",

        "api": {
            "id": api.id,
            "name": api.name,
            "status": api.status
        }
    }




@router.put(
    "/apis/{api_id}/reject"
)
def reject_api(
    api_id: int,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    api = db.query(
        API
    ).filter(
        API.id == api_id
    ).first()



    if not api:

        raise HTTPException(
            status_code=404,
            detail="API not found"
        )



    api.status = "rejected"



    db.commit()

    db.refresh(
        api
    )



    return {
        "message": "API rejected successfully",

        "api": {
            "id": api.id,
            "name": api.name,
            "status": api.status
        }
    }




@router.delete(
    "/reviews/{review_id}"
)
def delete_review(
    review_id: int,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )



    review = db.query(
        Review
    ).filter(
        Review.id == review_id
    ).first()



    if not review:

        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )



    db.delete(
        review
    )


    db.commit()



    return {
        "message": "Review deleted successfully"
    }