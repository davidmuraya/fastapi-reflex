from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


# Define Enum for valid Statuses
class StatusDescription(Enum):
    Delivered = "Delivered"
    Pending = "Pending"
    Cancelled = "Cancelled"


class SortBy(Enum):
    ascending = "asc"
    descending = "desc"


# SQLModel setup
class Customer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    phone: str
    address: str
    date: str
    payments: float
    status: StatusDescription

    # Config class to use enum values
    class Config:
        use_enum_values = True


# Customer update model
class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date: Optional[str] = None
    payments: Optional[float] = None
    status: Optional[StatusDescription] = None

    # Config class to use enum values
    class Config:
        use_enum_values = True
