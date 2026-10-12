import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient

# Override database.py before importing models
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')

@pytest.fixture(scope="session")
def db():
    """Create test database"""
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://devuser:testpass123@localhost:5432/saas_db')
    
    if 'sqlite' in DATABASE_URL:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DATABASE_URL)
    
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    
    yield SessionLocal()
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)
