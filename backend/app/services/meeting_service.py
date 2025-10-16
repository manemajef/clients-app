from sqlmodel import Session, select
from app.models.meeting import Meeting, MeetingCreate
from app.services.utils import utc_now
from app.services.client_service import client_exists_by_id
from app.services.user_service import get_user_by_id

def add_meeting(meeting: MeetingCreate, db:Session) -> Meeting | None:
    if get_user_by_id(meeting.user_id, db) is None:
        return None
    if meeting.client_id and not client_exists_by_id(meeting.user_id, meeting.client_id, db):
        return None
    db_meeting = Meeting(**meeting.model_dump())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting
