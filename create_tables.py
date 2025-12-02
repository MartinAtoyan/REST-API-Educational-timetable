from database import engine
from app.models.base import Base
import app.models  # noqa: F401, ensures all models are registered

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("✔ Tables created (if they did not already exist)")
