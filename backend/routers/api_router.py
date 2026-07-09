from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import (
    API,
    User,
    APIUsage,
    Review
)

from schemas.api_schema import (
    APICreate,
    APIResponse,
    APIUpdate
)

from services.auth import require_developer

from sqlalchemy import func


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
    search: str | None = None,
    category: str | None = None,
    pricing: str | None = None,
    sort_by: str | None = "newest",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(API)


    if search:
        query = query.filter(
            API.name.ilike(f"%{search}%")
        )


    if category:
        query = query.filter(
            API.category == category
        )


    if pricing:
        query = query.filter(
            API.pricing == pricing
        )


    if sort_by == "newest":
        query = query.order_by(
            API.created_at.desc()
        )


    elif sort_by == "oldest":
        query = query.order_by(
            API.created_at.asc()
        )


    offset = (page - 1) * limit


    apis = query.offset(
        offset
    ).limit(
        limit
    ).all()


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




@router.get(
    "/my-apis",
    response_model=list[APIResponse]
)
def get_my_apis(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_developer)
):

    apis = db.query(API).filter(
        API.developer_id == current_user.id
    ).all()


    return apis




@router.get(
    "/apis/discovery/popular"
)
def popular_apis(
    db: Session = Depends(get_db)
):


    results = (
        db.query(
            API.id,
            API.name,
            API.category,
            func.count(APIUsage.id).label(
                "total_requests"
            )
        )
        .join(
            APIUsage,
            API.id == APIUsage.api_id
        )
        .group_by(
            API.id
        )
        .order_by(
            func.count(APIUsage.id).desc()
        )
        .limit(10)
        .all()
    )


    return [
        {
            "api_id": item.id,
            "name": item.name,
            "category": item.category,
            "total_requests": item.total_requests
        }
        for item in results
    ]




@router.get(
    "/apis/discovery/top-rated"
)
def top_rated_apis(
    db: Session = Depends(get_db)
):


    results = (
        db.query(
            API.id,
            API.name,
            API.category,
            func.avg(Review.rating).label(
                "average_rating"
            ),
            func.count(Review.id).label(
                "total_reviews"
            )
        )
        .join(
            Review,
            API.id == Review.api_id
        )
        .group_by(
            API.id
        )
        .order_by(
            func.avg(Review.rating).desc()
        )
        .limit(10)
        .all()
    )


    return [
        {
            "api_id": item.id,
            "name": item.name,
            "category": item.category,
            "average_rating": round(
                item.average_rating,
                2
            ),
            "total_reviews": item.total_reviews
        }

        for item in results
    ]




@router.get(
    "/apis/discovery/recent"
)
def recent_apis(
    db: Session = Depends(get_db)
):


    apis = (
        db.query(API)
        .order_by(
            API.created_at.desc()
        )
        .limit(10)
        .all()
    )


    return [
        {
            "api_id": api.id,
            "name": api.name,
            "category": api.category,
            "pricing": api.pricing,
            "created_at": api.created_at
        }

        for api in apis
    ]