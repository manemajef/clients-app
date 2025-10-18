from sqlmodel import Session, select
from app.models.client import Client, Contact


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

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.flush()  # Get ID without committing
        self.db.refresh(client)
        return client

    def get_all_by_user_id(self, user_id: int) -> list[Client]:
        return self.db.exec(select(Client).where(Client.user_id == user_id)).all()

    def get_by_id(self, client_id: int) -> Client | None:
        return self.db.exec(select(Client).where(Client.id == client_id)).first()

    def get_by_user_and_name(self, user_id: int, name: str) -> Client | None:
        return self.db.exec(
            select(Client).where(
                (Client.user_id == user_id) & (Client.name == name)
            )
        ).first()

    def exists_for_user(self, client_id: int, user_id: int) -> bool:
        result = self.db.exec(
            select(Client.id).where(
                (Client.id == client_id) & (Client.user_id == user_id)
            )
        ).first()
        return result is not None
