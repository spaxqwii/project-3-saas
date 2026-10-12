import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env.local for local dev
load_dotenv('.env.local')

Base = declarative_base()

# Delay engine creation until it's actually needed
_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
        
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL not set")
        
        if 'sqlite' in DATABASE_URL:
            _engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(DATABASE_URL)
    
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()