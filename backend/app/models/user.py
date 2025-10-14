from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.services.utils import utc_now


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str | None = None 

class User(UserBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=utc_now)

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime | None = None


class UserLogin(BaseModel):
    email: str
    password: str

class UserVerify(BaseModel):
    access_token: str

class UserRefresh(BaseModel):
    refresh_token: str
