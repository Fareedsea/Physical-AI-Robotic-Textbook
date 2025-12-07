import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """
    Establishes a connection to the Neon Postgres database.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    
    try:
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error connecting to Postgres: {e}")
        raise e

def init_db():
    """
    Initializes the database schema (users, chat_history, etc.)
    """
    if not DATABASE_URL:
        print("WARNING: DATABASE_URL not set. Skipping DB initialization.")
        return

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255),
        password_hash VARCHAR(255),
        software_bg VARCHAR(50),
        hardware_bg VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # We can add more tables for chat history later
    
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(create_users_table)
            conn.commit()
            print("Database tables initialized.")
    except Exception as e:
        print(f"Database initialization failed: {e}")
