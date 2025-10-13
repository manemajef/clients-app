from sqlmodel import Session, select
from app.models.user import UserCreate, User
from fastapi import HTTPException
from app.core.security import hash_password, verify_password
from typing import Optional


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    return db.exec(select(User).where(User.email == email)).first()


def create_user(user: UserCreate, db: Session) -> User | None:
    if get_user_by_email(user.email, db):
        raise HTTPException(status_code=400, detail="Email is taken")
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user = get_user_by_email(email, db)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
