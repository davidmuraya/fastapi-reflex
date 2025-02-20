from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# SQLModel setup
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    password: str
    active: bool = True


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: str
    access_token: str


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expiry: Optional[str] = None
    expiry_date_time: Optional[str] = None
    error: Optional[str] = None
    message: Optional[str] = None
    success: Optional[bool] = None


class TokenData(BaseModel):
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str
