from repositories.user_repository import UserRepository
from repositories.client_repository import ClientRepository, ContactRepository
from repositories.meeting_repository import MeetingRepository
from app.services.client_service import ClientService
from app.services.meeting_service import MeetingService
from app.database import engine
from app.core.utils import utc_now
from app.models.client import ClientAdd
from app.models.meeting import MeetingCreate
from datetime import timedelta
from sqlmodel import Session

revenues = [1000, 300, 700]
durations = [1.0, 0.5, 1.5]
dates = [utc_now() + timedelta(days=d) for d in [8, 3, 1]]

def add_quick_client(name: str, client_service: ClientService) -> int | None:
    added = client_service.add_client("jeff", ClientAdd(name=name))
    if added:
        return added.id
    return None

def test_add_meeting():
    with Session(engine) as db:
        # Create repositories
        user_repo = UserRepository(db)
        client_repo = ClientRepository(db)
        contact_repo = ContactRepository(db)
        meeting_repo = MeetingRepository(db)

        # Create services
        client_service = ClientService(client_repo, contact_repo, user_repo)
        meeting_service = MeetingService(meeting_repo, user_repo, client_repo)

        # Get user
        user = user_repo.get_by_email("jeff")

        if not user:
            print("error: user 'jeff' not found")
            return

        user_id = user.id

        # Add clients and meetings
        for c in ["ron", "charles", "oded"]:
            client_id = add_quick_client(c, client_service)
            if not client_id:
                continue
                # only add a new meeting if a new client was added, since data is hard written,
                # to avoid duplications if script is accidentally rerun.

            meeting = MeetingCreate(
                revenue=revenues.pop(),
                date=dates.pop(),
                duration=durations.pop() or 1.0,
                user_id=user_id,
                client_id=client_id
            )
            added = meeting_service.add_meeting(meeting)
            print(f"Added meeting: Id={added.id if added else 'None'}")


if __name__ == "__main__":
    test_add_meeting()
