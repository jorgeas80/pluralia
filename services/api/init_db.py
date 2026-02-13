from sqlmodel import SQLModel, create_engine
# Ensure models are imported so they are in metadata
from services.api.src.infrastructure.database.models import SourceModel, ArticleModel, NewsGroupModel
import os

def init():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("No DATABASE_URL set")
        return
    engine = create_engine(url)
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init()
