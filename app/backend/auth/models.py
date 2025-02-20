from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


# SQLModel setup
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: EmailStr
    password: str
    active: bool = True


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
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
    email: EmailStr


# Model for updating a user; all fields are optional
class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: EmailStr | None = Field(default=None)
    password: Optional[str] = None
    active: Optional[bool] = None
