from sqlmodel import Session, select
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.exec(select(User).where(User.email == email)).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.exec(select(User).where(User.id == user_id)).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()  # Get ID without committing
        self.db.refresh(user)
        return user


    def get_all(self) -> list[User]:
        return self.db.exec(select(User)).all()
