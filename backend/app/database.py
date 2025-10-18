from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from app.models import user, client, meeting
# database_url = settings.DATABASE_URL
database_url = "sqlite:///app.db"
engine = create_engine(database_url, echo = False)


def create_tables():
    SQLModel.metadata.create_all(engine)

def get_sqlmodel_schema() -> dict:
    return SQLModel.metadata.tables.items()
