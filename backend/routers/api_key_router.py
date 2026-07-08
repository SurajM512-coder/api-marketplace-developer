from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import secrets

from database.db import get_db
from database.models import API, APIKey, Subscription, User

from schemas.api_key_schema import APIKeyResponse

from services.auth import get_current_user_data

from services.api_key_service import validate_api_key

from fastapi import Request

from services.usage_service import log_api_usage


router = APIRouter(
    tags=["API Keys"]
)


@router.post(
    "/api-keys/{api_id}",
    response_model=APIKeyResponse
)
def generate_api_key(
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

    
    subscription = db.query(Subscription).filter(
       Subscription.user_id == current_user.id,
       Subscription.api_id == api.id,
       Subscription.is_active == True
    ).first()


    if not subscription:
       raise HTTPException(
         status_code=403,
         detail="You must subscribe before generating an API key"
    )


    generated_key = secrets.token_urlsafe(32)


    new_key = APIKey(
        key=generated_key,
        user_id=current_user.id,
        api_id=api.id
    )


    db.add(new_key)
    db.commit()
    db.refresh(new_key)


    return new_key




@router.get(
    "/my-api-keys",
    response_model=list[APIKeyResponse]
)
def get_my_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):

    keys = db.query(APIKey).filter(
        APIKey.user_id == current_user.id
    ).all()


    return keys




@router.delete(
    "/api-keys/{key_id}"
)
def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):

    api_key = db.query(APIKey).filter(
        APIKey.id == key_id
    ).first()


    if not api_key:
        raise HTTPException(
            status_code=404,
            detail="API key not found"
        )


    if api_key.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to revoke this API key"
        )


    api_key.is_active = False


    db.commit()
    db.refresh(api_key)


    return {
        "message": "API key revoked successfully"
    }




@router.get(
    "/test-api-access"
)
def test_api_access(
    request: Request,
    api_key = Depends(validate_api_key),
    db: Session = Depends(get_db)
):


    log_api_usage(
        db=db,
        api_id=api_key.api_id,
        user_id=api_key.user_id,
        api_key_id=api_key.id,
        endpoint=str(request.url.path),
        method=request.method
    )


    return {
        "message": "API access granted",
        "api_id": api_key.api_id,
        "user_id": api_key.user_id
    }