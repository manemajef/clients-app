from repositories.user_repository import UserRepository
from repositories.client_repository import ClientRepository, ContactRepository
from app.services.client_service import ClientService
from app.database import engine
from sqlmodel import Session
from app.models.client import ContactBase, ClientAdd

user = "rotem"
clients = [
    ClientAdd(
        name = "bob"
    ),
    ClientAdd (
        name = "alice" ,
        contacts = [
            ContactBase (
                type = "phone", contact = "+972538713139"
            ),
            ContactBase (
                type = "email", contact = "alice@eatmyass.com"
            )
        ]
    )
]

def test_client_add():
    with Session(engine) as db:
        user_repo = UserRepository(db)
        client_repo = ClientRepository(db)
        contact_repo =ContactRepository(db)
        client_service = ClientService(client_repo, contact_repo, user_repo)
        for client in clients:
            added = client_service.add_client("jeff", client)
            print(added)
if __name__ == "__main__":
    test_client_add()
