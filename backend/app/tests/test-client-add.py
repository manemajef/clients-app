from app.services.user_service import add_client
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
        for client in clients:
            added = add_client(user, client, db)
            print(added)

if __name__ == "__main__":
    test_client_add()
