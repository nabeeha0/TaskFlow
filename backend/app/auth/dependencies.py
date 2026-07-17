from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.core.security import security

from app.database.dependencies import get_db

from app.auth.token import decode_access_token

from app.crud.user import get_user_by_email


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user