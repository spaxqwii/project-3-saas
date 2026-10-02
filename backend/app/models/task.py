from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    team_id = Column(Integer, ForeignKey("teams.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    created_at = Column(DateTime, default=datetime.utcnow)

    team = relationship("Team", back_populates="tasks")
    assigned_to_user = relationship("User", back_populates="tasks", foreign_keys=[assigned_to])
