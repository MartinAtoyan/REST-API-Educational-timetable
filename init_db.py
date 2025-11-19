import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

DB_NAME = os.getenv("APP_DB_NAME")
DB_USER = os.getenv("APP_DB_USER")
DB_PASSWORD = os.getenv("APP_DB_PASS")


def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"""
        DO $$
        BEGIN
           IF NOT EXISTS (
              SELECT FROM pg_roles WHERE rolname = '{DB_USER}'
           ) THEN
              CREATE ROLE {DB_USER} LOGIN PASSWORD '{DB_PASSWORD}';
           END IF;
        END
        $$;
    """)

    cur.execute(f"""
        DO $$
        BEGIN
           IF NOT EXISTS (
              SELECT FROM pg_database WHERE datname = '{DB_NAME}'
           ) THEN
              CREATE DATABASE {DB_NAME}
              WITH OWNER = {DB_USER}
                   ENCODING = 'UTF8'
                   TEMPLATE = template0;
           END IF;
        END
        $$;
    """)

    cur.close()
    conn.close()

    print("✔ Database initialized successfully!")


if __name__ == "__main__":
    create_database()
