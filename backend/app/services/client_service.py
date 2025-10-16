from app.models.client import Client, ClientAdd , ContactBase, ContactCreate , Contact
from sqlmodel import Session, select
from app.models.user import User
from app.services.user_service import get_user_by_email

def add_client(user_email: str, client: ClientAdd, db: Session) -> Client | None:
    user = get_user_by_email(user_email, db)
    if not user:
        return None
    name = client.name
    conflict_client = db.exec(select(Client).where((Client.name == name) & (Client.user_id == user.id))).first()
    if conflict_client:
        return None
    client_create = Client(
        name = client.name,
        user_id =  user.id
    )
    db.add(client_create)
    db.flush()
    db.refresh(client_create)
    for contact in client.contacts:
        add_contect_by_client_id(contact, client_create.id,db )
    db.commit()
    return client_create

def add_contect_by_client_id(contact: ContactBase, client_id: int | None , db: Session) -> Contact | None:
    if client_id is None:
        return None
    contact = Contact(
        type = contact.type ,
        contact = contact.contact ,
        client_id = client_id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
def get_client_by_id(id: int, db: Session) -> Client | None:
    client = db.exec(select(Client).where(Client.id == id)).first()
    if not client:
        return None
    return client

def get_clients_user(client: Client, db: Session) -> User | None:
    user = db.exec(select(User).where(User.id == client.user_id)).first()
    if not user:
        return None
    return user

def client_exists_by_id(user_id: int, client_id: int, db: Session) -> bool:
    client = get_client_by_id(client_id, db)
    if not client:
        return False
    return client.user_id == user_id

def get_client_by_name(email: str, name: str, db: Session) -> Client | None:
    user = get_user_by_email(email, db)
    if not user:
        return None
    user_id = user.id
    return db.exec(select(Client).where((Client.user_id == user_id) & (Client.name == name))).first()
