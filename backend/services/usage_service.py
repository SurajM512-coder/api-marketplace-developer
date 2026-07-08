from sqlalchemy.orm import Session

from database.models import APIUsage


def log_api_usage(
    db: Session,
    api_id: int,
    user_id: int,
    api_key_id: int,
    endpoint: str,
    method: str
):


    usage = APIUsage(
        api_id=api_id,
        user_id=user_id,
        api_key_id=api_key_id,
        endpoint=endpoint,
        method=method
    )


    db.add(usage)

    db.commit()

    db.refresh(usage)


    return usage