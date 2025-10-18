from sqlmodel import Session, select
from app.models.user import User , UserCreate
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_by_email(self, email: str) -> User | None:
        return self.db.exec(select(User).where(User.email == email)).first()
    def get_by_id(self, id: str) -> User | None:
        return self.db.exec(select(User).where(User.id == id)).first()
    def create(self, user: User) -> User | None:
        user_add = User(**user.model_dump())
        self.db.add(user_add)
        self.db.commit()
        self.db.refresh(user_add)
        return user
