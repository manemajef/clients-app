from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from app.models import user, client, meeting 
database_url = settings.DATABASE_URL
engine = create_engine(database_url, echo = False)


def create_tables():
    SQLModel.metadata.create_all(engine)

# def get_db():
#     with Session(engine) as db:
#         yield db

# if __name__ == "__main__":
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT 'connected!'"))
#     print(result.scalar())
#
