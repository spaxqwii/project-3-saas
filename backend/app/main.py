from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.database import get_db
from app.models import User, Task
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secrets (move to .env later)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# 1. REGISTER
@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # TODO: implement bcrypt properly
    # For now, store password in plain text (TESTING ONLY)
    new_user = User(email=user.email, username=user.username, password_hash=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}

# 2. LOGIN
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    # TODO: implement bcrypt properly
    # For now, compare passwords in plain text (TESTING ONLY)
    if not db_user or db_user.password_hash != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"sub": str(db_user.id), "exp": datetime.utcnow() + timedelta(hours=24)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}

# 3. GET TASKS (placeholder—returns empty list for now)
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]

@app.get("/health")
def health():
    return {"status": "ok"}
