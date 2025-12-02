from database import engine

# Import each model module's Base (they each define their own declarative Base)
from app.models.lesson import Base as lesson_base
from app.models.teacher import Base as teacher_base
from app.models.subject import Base as subject_base


def create_tables():
    # Create tables for each Base's metadata
    lesson_base.metadata.create_all(bind=engine)
    teacher_base.metadata.create_all(bind=engine)
    subject_base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("✔ Tables created (if they did not already exist)")
