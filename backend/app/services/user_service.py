from sqlmodel import Session, select
from app.models.user import UserCreate, User
from app.models.client import Client, ClientCreate, ClientBase,  ContactBase, ClientAdd , Contact
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, decode_access_token
from typing import Optional


def get_user_by_email(email: str, db: Session) -> User | None:
    return db.exec(select(User).where(User.email == email)).first()


def create_user(user: UserCreate, db: Session) -> User | None:
    if get_user_by_email(user.email, db):
        raise HTTPException(status_code=400, detail="Email is taken")
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user = get_user_by_email(email, db)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_token(token: str, db:Session) -> User | None:
    email = decode_access_token(token)
    if not email:
        return None
    return get_user_by_email(email, db)


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
