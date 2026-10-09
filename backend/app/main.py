from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import logging
from app.database import get_db
from app.models import User, Task
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

class UserRegister(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {user.email}")
    
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        logger.warning(f"Registration failed - email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(email=user.email, username=user.username, password_hash=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User registered successfully: {user.email} (ID: {new_user.id})")
    return {"id": new_user.id, "email": new_user.email}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {user.email}")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password_hash != user.password:
        logger.warning(f"Login failed for email: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"sub": str(db_user.id), "exp": datetime.utcnow() + timedelta(hours=24)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    logger.info(f"User logged in successfully: {user.email}")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    logger.info(f"Tasks retrieved: {len(tasks)} tasks found")
    return [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]

@app.get("/health")
def health():
    logger.info("Health check")
    return {"status": "ok"}