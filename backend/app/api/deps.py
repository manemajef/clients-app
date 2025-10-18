from sqlmodel import Session
from app.database import engine
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.core.security import decode_access_token
from app.services.user_service import get_user_by_email
from app.models.user import User
# from typing import Annotated


def get_db():
    with Session(engine) as db:
        yield db


security = HTTPBearer()



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
