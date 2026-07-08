from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from database.db import get_db

from database.models import (
    Review,
    API,
    User,
    Subscription
)


from schemas.review_schema import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)


from services.auth import get_current_user_data

from sqlalchemy import func



router = APIRouter(
    tags=["Reviews"]
)



@router.post(
    "/reviews/{api_id}",
    response_model=ReviewResponse
)
def create_review(
    api_id: int,
    review: ReviewCreate,
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
          detail="Subscribe before reviewing this API"
        )


    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.api_id == api.id
    ).first()


    if existing_review:
        raise HTTPException(
           status_code=400,
           detail="You have already reviewed this API"
        )


    new_review = Review(
        user_id=current_user.id,
        api_id=api.id,
        rating=review.rating,
        comment=review.comment
    )


    db.add(new_review)

    db.commit()

    db.refresh(new_review)


    return new_review




@router.get(
    "/reviews/{api_id}",
    response_model=list[ReviewResponse]
)
def get_reviews(
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


    reviews = db.query(Review).filter(
        Review.api_id == api.id
    ).all()


    return reviews




@router.put(
    "/reviews/{review_id}",
    response_model=ReviewResponse
)
def update_review(
    review_id: int,
    updated_review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    review = db.query(Review).filter(
        Review.id == review_id
    ).first()


    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )


    if (
        review.user_id != current_user.id
        and current_user.role.value != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed to edit this review"
        )


    for key, value in updated_review.dict(
        exclude_unset=True
    ).items():

        setattr(
            review,
            key,
            value
        )


    db.commit()

    db.refresh(review)


    return review




@router.delete(
    "/reviews/{review_id}"
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_data)
):


    review = db.query(Review).filter(
        Review.id == review_id
    ).first()


    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )


    if (
        review.user_id != current_user.id
        and current_user.role.value != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed to delete this review"
        )


    db.delete(review)

    db.commit()


    return {
        "message": "Review deleted successfully"
    }




@router.get(
    "/reviews/{api_id}/summary"
)
def review_summary(
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


    result = db.query(
        func.avg(Review.rating),
        func.count(Review.id)
    ).filter(
        Review.api_id == api.id
    ).first()


    average_rating = result[0]

    total_reviews = result[1]


    return {
        "api_id": api.id,
        "api_name": api.name,
        "average_rating": round(
            average_rating,
            2
        ) if average_rating else 0,
        "total_reviews": total_reviews
    }