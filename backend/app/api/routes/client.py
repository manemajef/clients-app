from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.models.client import *
from app.api.deps import get_current_user, get_db

router = APIRouter(
    prefix = "/clients",
    tags = ["clients"],
    dependencies = [Depends(get_current_user),Depends(get_db)],
    responses = {404: {'description': 'Not found'}}
)
