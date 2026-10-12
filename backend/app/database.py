import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv('.env.local')

Base = declarative_base()

def get_db():
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set")
    
    if 'sqlite' in DATABASE_URL:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DATABASE_URL)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()