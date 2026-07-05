from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import APIKey


def validate_api_key(
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):

    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )


    api_key = db.query(APIKey).filter(
        APIKey.key == x_api_key
    ).first()


    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )


    if not api_key.is_active:
        raise HTTPException(
            status_code=403,
            detail="API key revoked"
        )


    return api_key




