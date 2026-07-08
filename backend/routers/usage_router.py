from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


from database.db import get_db

from database.models import (
    APIUsage,
    User,
    API
)


from schemas.usage_schema import UsageResponse


from services.auth import get_current_user_data


from sqlalchemy import func



router = APIRouter(
    tags=["Usage Analytics"]
)



@router.get(
    "/my-usage",
    response_model=list[UsageResponse]
)
def get_my_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    usage = db.query(APIUsage).filter(
        APIUsage.user_id == current_user.id
    ).all()


    return usage




@router.get(
    "/developer-usage"
)
def developer_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    results = (
        db.query(
            APIUsage.api_id,
            API.name.label("api_name"),
            func.count(APIUsage.id).label("total_requests")
        )
        .join(
            API,
            API.id == APIUsage.api_id
        )
        .filter(
            API.developer_id == current_user.id
        )
        .group_by(
            APIUsage.api_id,
            API.name
        )
        .all()
    )


    return [
        {
          "api_id": item.api_id,
          "api_name": item.api_name,
          "total_requests": item.total_requests
        }
        for item in results
   ]