from sqlmodel import SQLModel, Field, Relationship 
from pydantic import BaseModel 
from typing import TYPE_CHECKING 
from app.services.utils import utc_now 
from datetime import datetime 

if TYPE_CHECKING:
    from app.models.client import Client 
    from app.models.user import User 
    
class MeetingCreate(SQLModel):
    revenue: int | None = 0 
    date: datetime | None = Field(default_factory=utc_now)
    duration: float | None = 1.0
    client_id: int | None = Field(default=None,foreign_key="client.id") 
    user_id: int = Field(foreign_key="user.id")
    
class Meeting(MeetingCreate, table = True):
    id: int | None = Field(default=None, primary_key=True) 
    client: 'Client' = Relationship(back_populates="meetings")
    user: 'User' = Relationship(back_populates="meetings")

