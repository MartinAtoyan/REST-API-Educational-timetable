from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Read DB connection info from environment with sensible defaults
DB_USER = os.getenv("APP_DB_USER", "timetable_user")
DB_PASS = os.getenv("APP_DB_PASS", "password123")
DB_NAME = os.getenv("APP_DB_NAME", "timetable_db")
DB_HOST = os.getenv("APP_DB_HOST", "localhost")
DB_PORT = os.getenv("APP_DB_PORT", "5432")

DATABASE_URL = os.getenv(
	"DATABASE_URL",
	f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
