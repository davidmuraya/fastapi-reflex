from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, String, asc, cast, desc, or_, select

from app.backend.database.utils import get_session

router = APIRouter(prefix="/api")


# SQLModel setup
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    password: str


@router.get("/users/{email}", response_model=User)
def get_user(email: str, session: Session = Depends(get_session)):
    """
    This is just an example of how to retrieve a user from the database.
    In a real application, you would want to implement some kind of authentication
    and authorization mechanism to ensure that only authorized users can access certain resources.
    """
    user = session.get(User, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
