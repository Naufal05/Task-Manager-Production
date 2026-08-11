from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field

class PriorityEnum(str, Enum):
    """
    A plain Python Enum, made JSON-friendly by also inheriting from `str`.
    FastAPI/Pydantic will automatically:
      - validate incoming values against these choices
      - show a dropdown of valid options in the Swagger docs (/docs)
      - reject anything that isn't 'low', 'medium', or 'high' with a 422 error
    """
    low = "low"
    medium = "medium"
    high = "high"



class TaskBase(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    due_date: Optional[datetime] = Field(default=None)
    tags: Optional[str] = Field(default=None, max_length=200)

class Task(TaskBase, table=True):
    """
    table=True tells SQLModel: 'this class is also a real database table.'
    This is the class Alembic will look at to generate migrations,
    and the class we'll use when querying/inserting/updating rows.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    """
    What a client sends us when CREATING a task via POST.
    Notice: no 'id' or 'created_at' — the client doesn't get to set those,
    the database/server decides them.
    """
    pass


class TaskUpdate(SQLModel):
    """
    What a client sends us when UPDATING a task via PATCH.
    Every field is Optional — a client might only want to update
    'completed', without resending title/description/etc.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """
    What we SEND BACK to the client as a response.
    Includes id and created_at, which are server-generated.
    """
    id: int
    created_at: datetime


# ---------------------------------------------------------------------------
# AUTH MODELS
# ---------------------------------------------------------------------------
 
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)


class User(UserBase, table=True):
    """
    The real 'user' database table. Notice: NO plaintext 'password' field --
    only 'hashed_password'. We NEVER store or even temporarily hold onto a
    plaintext password beyond the single request where it's first received.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    """What a client sends to POST /auth/register -- plaintext password,
    accepted ONLY here, hashed immediately, then discarded."""
    password: str = Field(min_length=8)


class UserRead(UserBase):
    """What we send back after registration/lookup -- notice hashed_password
    is deliberately excluded, so we never leak even the HASH to clients."""
    id: int
    created_at: datetime

class Token(SQLModel):
    """Response shape for a successful login."""
    access_token: str
    token_type: str = "bearer"