from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.models.user import UserCreate, UserResponse, UserLogin, User
from pydantic import BaseModel
from app.services.user_service import UserService
from app.api.deps import get_db, get_current_user, get_user_service
from app.core.security import create_access_token, create_refresh_token, refresh_token
from app.models.token import TokenResponse


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    print("DEBUG:", type(user.password), repr(user.password))

    return user_service.create_user(user)


@router.post("/login", response_model=TokenResponse)
def login(login: UserLogin, user_service: UserService = Depends(get_user_service)):
    user = user_service.authenticate_user(login.email, login.password)
    if not user:
        raise HTTPException(status_code=401)
    token_data = {"sub": user.email}
    access_token = create_access_token(token_data)
    refresh= create_refresh_token(token_data)
    return {"access_token": access_token, "refresh_token": refresh}


@router.post("/refresh", response_model=TokenResponse)
def new_refresh_token(token: str = Depends(oauth2_schema)):
    new_token = refresh_token(token)
    if not new_token:
        raise HTTPException(status_code=401)
    return {"access_token": new_token, "refresh_token": token}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
