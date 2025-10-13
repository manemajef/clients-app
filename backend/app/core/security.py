from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional
from app.services.utils import utc_now 
pwd_context = CryptContext(schemas=["bcrypt"], deprecated="auto")


# == password ==
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# == token create ==
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = utc_now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = utc_now() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# == token decode ==
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if not payload.get("type", None) == "access":
            return None
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None


def decode_refresh_token(token: str) -> str | None:
    try:
        p: dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if p.get("type") != "refresh":
            return None
        email = p.get("sub")
        return create_access_token({"sub": email})
    except JWTError:
        return None


def refresh_token(token: str) -> str | None:
    return decode_refresh_token(token)
