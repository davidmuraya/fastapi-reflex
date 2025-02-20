from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, String, asc, cast, desc, or_, select

from app.backend.database.utils import get_session

router = APIRouter(prefix="/api")


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


# API endpoints
@router.get("/customers", response_model=List[Customer], tags=["Customer"])
async def get_customers(
    session: Session = Depends(get_session),
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
):
    query = select(Customer)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            or_(
                Customer.name.ilike(search_filter),
                Customer.email.ilike(search_filter),
                Customer.phone.ilike(search_filter),
                Customer.address.ilike(search_filter),
                cast(Customer.payments, String).ilike(search_filter),
                Customer.status.ilike(search_filter),
            )
        )

    if sort_by:
        column = getattr(Customer, sort_by, None)
        if not column:
            raise HTTPException(400, "Invalid sort column")
        query = query.order_by(desc(column) if sort_order == "desc" else asc(column))

    return session.exec(query).all()


@router.get("/customers/{customer_id}", response_model=Customer, tags=["Customer"])
def get_customer(customer_id: int, session: Session = Depends(get_session)):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/customers", response_model=List[Customer], tags=["Customer"])
def add_customers(customers: List[Customer], session: Session = Depends(get_session)):
    # First, verify that none of the customer IDs already exist.
    for customer in customers:
        if session.get(Customer, customer.id):
            raise HTTPException(
                status_code=400, detail=f"Customer ID {customer.id} already exists"
            )

    # Add all customers to the session
    for customer in customers:
        session.add(customer)

    # Commit once after adding all customers
    session.commit()

    # Refresh each customer instance so that we have the latest DB state
    for customer in customers:
        session.refresh(customer)

    return customers


@router.delete("/customers/{customer_id}", response_model=dict, tags=["Customer"])
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted successfully"}


@router.put("/customers/{customer_id}", response_model=Customer, tags=["Customer"])
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    session: Session = Depends(get_session),
):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)

    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
