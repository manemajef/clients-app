from sqlmodel import Session, select
from app.models.meeting import Meeting


class MeetingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, meeting_id: int) -> Meeting | None:
        return self.db.exec(select(Meeting).where(Meeting.id == meeting_id)).first()

    def get_all_by_client_id(self, client_id: int) -> list[Meeting]:
        return self.db.exec(select(Meeting).where(Meeting.client_id == client_id)).all()

    def get_all_by_user_id(self, user_id: int) -> list[Meeting]:
        return self.db.exec(select(Meeting).where(Meeting.user_id == user_id)).all()

    def create(self, meeting: Meeting) -> Meeting:
        self.db.add(meeting)
        self.db.flush()
        self.db.refresh(meeting)
        return meeting
