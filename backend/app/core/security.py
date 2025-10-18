# from passlib.context import CryptContext
import bcrypt
import jwt
from jwt import PyJWTError as JWTError
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional
from app.core.utils import utc_now

# pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


# == password ==
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


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
