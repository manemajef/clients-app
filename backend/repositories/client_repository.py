from sqlmodel import Session, select
from app.models.client import  Client, ClientAdd, Contact, ContactBase, ContactCreate


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, contact: Contact) -> Contact:
        self.db.add(contact)
        self.db.flush()
        self.db.refresh(contact)
        return contact

    def create_many(self, contacts: list[Contact]) -> list[Contact]:
        self.db.add_all(contacts)
        self.db.flush()
        for contact in contacts:
            self.db.refresh(contact)
        return contacts

    def get_by_client_id(self, client_id: int) -> list[Contact]:
        return self.db.exec(
            select(Contact).where(Contact.client_id == client_id)
        ).all()

    def get_by_id(self, contact_id: int) -> Contact | None:
        return self.db.exec(
            select(Contact).where(Contact.id == contact_id)
        ).first()


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_by_id(self, id:str) -> Client | None:
        return self.db.exec(select(Client).where(Client.id == id)).first()
