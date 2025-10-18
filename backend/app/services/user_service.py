from app.models.user import UserCreate, User
from app.core.security import hash_password, verify_password, decode_access_token
from repositories.user_repository import UserRepository
from fastapi import HTTPException


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_email(email)

    def get_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def create_user(self, user: UserCreate) -> User:
        # Check if email is already taken
        if self.user_repo.get_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email is taken")

        # Create user with hashed password
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hash_password(user.password),
        )
        created_user = self.user_repo.create(db_user)

        # Commit transaction at service level
        self.user_repo.db.commit()

        return created_user

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_user_by_token(self, token: str) -> User | None:
        email = decode_access_token(token)
        if not email:
            return None
        return self.user_repo.get_by_email(email)

    def get_all_users(self) -> list[User]:
        return self.user_repo.get_all()
