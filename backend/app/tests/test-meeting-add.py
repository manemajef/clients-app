from app.services.meeting_service import add_meeting
from app.database import engine
from app.services.client_service import add_client
from sqlmodel import Session , select
from app.models.meeting import MeetingCreate
from app.models.client import ClientAdd, Client
from app.models.user import User
from app.services.utils import utc_now
from datetime import datetime, timedelta


revenues = [1000, 300, 700]
durations = [1.0, 0.5, 1.5]
dates = [utc_now() + timedelta(days = d) for d in [8,3,1]]

def add_quick_client(name: str, db:Session) -> int | None:
    added = add_client("rotem", ClientAdd(name = name),db)
    if added:
        return added.id
    return None


def test_add_meeting():
    with Session(engine) as db:
        user = db.exec(select(User).where(User.email == "rotem")).first()
        if not user:
            print("error")
            return
        user_id = user.id
        for c in ["ron", "charles", "oded"]:
            client_id = add_quick_client(c, db)
            if not client_id:
                continue
                # only add a new meeting if a new client was added, since data is hard writen, to avoid duplications if script is accidently rerun.
            meeting = MeetingCreate (
                revenue = revenues.pop(),
                date = dates.pop(),
                duration = durations.pop() or 1.0 ,
                user_id = user_id ,
                client_id = client_id
            )
            added = add_meeting(meeting, db)
            print(f"Added meeting: Id= {added}")
if __name__ == "__main__":
    test_add_meeting()
