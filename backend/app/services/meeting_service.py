from app.models.meeting import Meeting, MeetingCreate
from repositories.meeting_repository import MeetingRepository
from repositories.user_repository import UserRepository
from repositories.client_repository import ClientRepository


class MeetingService:
    def __init__(
        self,
        meeting_repo: MeetingRepository,
        user_repo: UserRepository,
        client_repo: ClientRepository
    ):
        self.meeting_repo = meeting_repo
        self.user_repo = user_repo
        self.client_repo = client_repo

    def add_meeting(self, meeting: MeetingCreate) -> Meeting | None:
        # Validate user exists
        user = self.user_repo.get_by_id(meeting.user_id)
        if not user:
            return None

        # Validate client ownership if client_id is provided
        if meeting.client_id:
            client = self.client_repo.get_by_id(meeting.client_id)
            if not client or client.user_id != meeting.user_id:
                return None

        # Create meeting
        db_meeting = Meeting(**meeting.model_dump())
        created_meeting = self.meeting_repo.create(db_meeting)

        # Commit transaction
        self.meeting_repo.db.commit()

        return created_meeting

    def get_meeting_by_id(self, meeting_id: int) -> Meeting | None:
        return self.meeting_repo.get_by_id(meeting_id)

    def get_meetings_by_user_id(self, user_id: int) -> list[Meeting]:
        return self.meeting_repo.get_all_by_user_id(user_id)

    def get_meetings_by_client_id(self, client_id: int) -> list[Meeting]:
        return self.meeting_repo.get_all_by_client_id(client_id)
