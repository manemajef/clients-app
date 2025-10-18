from sqlmodel import Session
from app.database import engine
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.core.security import decode_access_token
from app.models.user import User

# Import repositories
from repositories.user_repository import UserRepository
from repositories.client_repository import ClientRepository, ContactRepository
from repositories.meeting_repository import MeetingRepository

# Import services
from app.services.user_service import UserService
from app.services.client_service import ClientService
from app.services.meeting_service import MeetingService


# Database session dependency
def get_db():
    with Session(engine) as db:
        yield db


# Repository dependencies
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_client_repository(db: Session = Depends(get_db)) -> ClientRepository:
    return ClientRepository(db)


def get_contact_repository(db: Session = Depends(get_db)) -> ContactRepository:
    return ContactRepository(db)


def get_meeting_repository(db: Session = Depends(get_db)) -> MeetingRepository:
    return MeetingRepository(db)


# Service dependencies
def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repo)


def get_client_service(
    client_repo: ClientRepository = Depends(get_client_repository),
    contact_repo: ContactRepository = Depends(get_contact_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> ClientService:
    return ClientService(client_repo, contact_repo, user_repo)


def get_meeting_service(
    meeting_repo: MeetingRepository = Depends(get_meeting_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    client_repo: ClientRepository = Depends(get_client_repository)
) -> MeetingService:
    return MeetingService(meeting_repo, user_repo, client_repo)


# Authentication
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
) -> User:
    token = credentials.credentials
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = user_service.get_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
