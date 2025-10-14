from sqlmodel import select
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models import user
from app.models.user import User, UserResponse
from app.api.deps import get_db, get_current_user
from app.core.config import settings 

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def get_users(secret: str, db: Session = Depends(get_db)):
    if not secret == settings.ADMIN_SECRET:
        return {"error": "no acces"}

    all_users = db.exec(select(User)).all()
    users = {}
    for u in all_users:
        users[u.id] = u
    return {"Users": users}

@router.get("/db") 
def get_db():
    return {"url": settings.DATABASE_URL}