from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from database.db import get_db

from database.models import (
    API,
    Subscription,
    User
)


from schemas.subscription_schema import SubscriptionResponse


from services.auth import get_current_user_data



router = APIRouter(
    tags=["Subscriptions"]
)



@router.post(
    "/subscribe/{api_id}",
    response_model=SubscriptionResponse
)
def subscribe_api(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    api = db.query(API).filter(
        API.id == api_id
    ).first()


    if not api:
        raise HTTPException(
            status_code=404,
            detail="API not found"
        )

    existing_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.api_id == api.id,
        Subscription.is_active == True
    ).first()


    if existing_subscription:
     raise HTTPException(
        status_code=400,
        detail="Already subscribed to this API"
    )


    inactive_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.api_id == api_id,
        Subscription.is_active == False
    ).first()


    if inactive_subscription:
       inactive_subscription.is_active = True

       db.commit()
       db.refresh(inactive_subscription)

       return inactive_subscription


    subscription = Subscription(
        user_id=current_user.id,
        api_id=api.id
    )


    db.add(subscription)

    db.commit()

    db.refresh(subscription)


    return subscription




@router.get(
    "/my-subscriptions",
    response_model=list[SubscriptionResponse]
)
def get_my_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).all()


    return subscriptions




@router.delete(
    "/subscriptions/{subscription_id}"
)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()


    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )


    if subscription.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot cancel this subscription"
        )


    subscription.is_active = False

    db.commit()
    db.refresh(subscription)


    return {
        "message": "Subscription cancelled successfully"
    }