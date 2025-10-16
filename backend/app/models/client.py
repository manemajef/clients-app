from sqlmodel import SQLModel, Field, Relationship
# from app.models.user import User
from pydantic import BaseModel
from typing import TYPE_CHECKING
# from app.models.user import User

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.meeting import Meeting



class ClientBase(SQLModel):
    name: str

class ClientCreate(ClientBase):
    user_id: int = Field(foreign_key="user.id")

class Client(ClientCreate, table = True):
    id: int | None  = Field(default=None, primary_key=True)
    user: 'User' = Relationship(back_populates="clients")
    contacts: list["Contact"] = Relationship(back_populates="client")
    meetings: list['Meeting'] = Relationship(back_populates="client")


class ContactBase(SQLModel):
    type: str | None = Field(default="else")
    contact: str

class ContactCreate(ContactBase):
    client_id: int = Field(foreign_key="client.id")

class Contact(ContactCreate, table = True):
    id: int | None = Field(default=None, primary_key=True)
    client: Client = Relationship(back_populates="contacts")

class ClientAdd(ClientBase):
    contacts: list[ContactBase] = Field(default_factory = list)
