from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, select

from app.backend.database.utils import get_session

router = APIRouter(prefix="/api")


# SQLModel setup
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: str


@router.post("/auth/login", response_model=UserLoginResponse)
def login_user(login_data: UserLoginRequest, session: Session = Depends(get_session)):
    """
    This is just an example of how to retrieve a user from the database.

    """

    # exception:
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found. Please check the spelling.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Get the user from the database
    db_user = session.exec(select(User).where(User.email == login_data.email)).first()

    # If the user doesn't exist, raise an exception
    if not db_user:
        raise user_not_found_exception

    # You likely need to hash and verify the password instead of comparing it directly
    if not db_user.password == login_data.password:
        raise invalid_credentials_exception

    # Return the user data
    user_data_response = UserLoginResponse(
        id=db_user.id, name=db_user.name, email=db_user.email
    )
    return user_data_response
