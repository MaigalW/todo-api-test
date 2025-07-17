from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus

class TaskCreate(TaskBase):
    #owner_id: Optional[str] = None
    pass

class Task(TaskBase):
    id: Optional[str] = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    owner_id: Optional[str] = None

