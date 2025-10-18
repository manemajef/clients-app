from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User, UserResponse
from app.api.deps import get_current_user, get_user_service
from app.services.user_service import UserService
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def get_users(secret: str, user_service: UserService = Depends(get_user_service)):
    if not secret == settings.ADMIN_SECRET:
        return {"error": "no acces"}

    all_users = user_service.get_all_users()
    users = {}
    for u in all_users:
        users[u.id] = u
    return {"Users": users}

@router.get("/db")
def get_db():
    return {"url": settings.DATABASE_URL}
