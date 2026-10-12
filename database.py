import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env.local for local dev
load_dotenv('.env.local')

# Get DATABASE_URL from environment, or use SQLite for testing
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')

# Create engine
if 'sqlite' in DATABASE_URL:
    # SQLite needs special handling
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL
    engine = create_engine(
        DATABASE_URL,
        poolclass=None,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()