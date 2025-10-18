from app.models.client import Client, ClientAdd, ContactBase, Contact
from repositories.client_repository import ClientRepository, ContactRepository
from repositories.user_repository import UserRepository


class ClientService:
    def __init__(
        self,
        client_repo: ClientRepository,
        contact_repo: ContactRepository,
        user_repo: UserRepository
    ):
        self.client_repo = client_repo
        self.contact_repo = contact_repo
        self.user_repo = user_repo

    def add_client(self, user_email: str, client: ClientAdd) -> Client | None:
        # Validate user exists
        user = self.user_repo.get_by_email(user_email)
        if not user:
            return None

        # Check for duplicate client name for this user
        conflict_client = self.client_repo.get_by_user_and_name(user.id, client.name)
        if conflict_client:
            return None

        # Create client
        client_create = Client(
            name=client.name,
            user_id=user.id
        )
        created_client = self.client_repo.create(client_create)

        # Create contacts for the client
        contacts = [
            Contact(
                type=contact.type,
                contact=contact.contact,
                client_id=created_client.id
            )
            for contact in client.contacts
        ]
        if contacts:
            self.contact_repo.create_many(contacts)

        # Commit transaction at service level
        self.client_repo.db.commit()

        return created_client

    def add_contact_by_client_id(self, contact: ContactBase, client_id: int) -> Contact | None:
        # Validate client exists
        client = self.client_repo.get_by_id(client_id)
        if not client:
            return None

        # Create contact
        contact_obj = Contact(
            type=contact.type,
            contact=contact.contact,
            client_id=client_id
        )
        created_contact = self.contact_repo.create(contact_obj)

        # Commit transaction
        self.contact_repo.db.commit()

        return created_contact

    def get_client_by_id(self, client_id: int) -> Client | None:
        return self.client_repo.get_by_id(client_id)

    def get_client_by_name(self, email: str, name: str) -> Client | None:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        return self.client_repo.get_by_user_and_name(user.id, name)

    def client_exists_for_user(self, user_id: int, client_id: int) -> bool:
        return self.client_repo.exists_for_user(client_id, user_id)

    def get_clients_by_user_id(self, user_id: int) -> list[Client]:
        return self.client_repo.get_all_by_user_id(user_id)

    def get_contacts_by_client_id(self, client_id: int) -> list[Contact]:
        return self.contact_repo.get_by_client_id(client_id)
