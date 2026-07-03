from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import API, User

from schemas.api_schema import (
    APICreate,
    APIResponse,
    APIUpdate
)

from services.auth import require_developer


router = APIRouter(
    tags=["APIs"]
)


@router.post(
    "/apis",
    response_model=APIResponse
)
def create_api(
    api: APICreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_developer)
):

    new_api = API(
        name=api.name,
        description=api.description,
        base_url=api.base_url,
        category=api.category,
        version=api.version,
        pricing=api.pricing,
        developer_id=current_user.id
    )

    db.add(new_api)
    db.commit()
    db.refresh(new_api)

    return new_api




@router.get(
    "/apis",
    response_model=list[APIResponse]
)
def get_all_apis(
    db: Session = Depends(get_db)
):

    apis = db.query(API).all()

    return apis




@router.get(
    "/apis/{api_id}",
    response_model=APIResponse
)
def get_api(
    api_id: int,
    db: Session = Depends(get_db)
):

    api = db.query(API).filter(
        API.id == api_id
    ).first()

    if not api:
        raise HTTPException(
            status_code=404,
            detail="API not found"
        )

    return api




@router.put(
    "/apis/{api_id}",
    response_model=APIResponse
)
def update_api(
    api_id: int,
    updated_api: APIUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_developer)
):

    api = db.query(API).filter(
        API.id == api_id
    ).first()


    if not api:
        raise HTTPException(
            status_code=404,
            detail="API not found"
        )


    if (
        api.developer_id != current_user.id
        and current_user.role.value != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed to update this API"
        )


    for key, value in updated_api.dict(exclude_unset=True).items():
        setattr(api, key, value)


    db.commit()
    db.refresh(api)

    return api




@router.delete(
    "/apis/{api_id}"
)
def delete_api(
    api_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_developer)
):

    api = db.query(API).filter(
        API.id == api_id
    ).first()


    if not api:
        raise HTTPException(
            status_code=404,
            detail="API not found"
        )


    if (
        api.developer_id != current_user.id
        and current_user.role.value != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed to delete this API"
        )


    db.delete(api)
    db.commit()


    return {
        "message": "API deleted successfully"
    }