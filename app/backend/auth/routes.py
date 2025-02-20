from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, String, asc, cast, desc, or_, select

from app.backend.auth.auth import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.backend.auth.models import (
    Token,
    User,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdate,
)
from app.backend.database.utils import get_session

router = APIRouter(prefix="/api/v1")


@router.post("/auth/login", response_model=UserLoginResponse, tags=["Authentication"])
def login_user(login_data: UserLoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate a user by checking their username and password

    """

    # Get the user from the database
    db_user = authenticate_user(email=login_data.email, password=login_data.password)

    # Create the access_token:
    access_token = create_access_token(data={"sub": db_user.email}, scope="app")

    # Return the user data
    user_data_response = UserLoginResponse(
        id=db_user.id, name=db_user.name, email=db_user.email, access_token=access_token
    )
    return user_data_response


@router.post(
    "/token", response_model=Token, tags=["Authentication"], summary="👤 Get token"
)
async def login_for_access_token(
    response: Response,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    # Endpoint to log in a user and provide an access token.

    🛡️ This endpoint authenticates a user using their username and password, retrieves the user's IP address
    and geo-location, and creates an access token if the credentials are correct and the user account is active.

    ### Params:

        🔓 username: The username you created the account with.
        🔓 password: Your account password.

    ### Returns:

        Token: A Token object containing the access token, token type, expiry time, and success status.

    ### Raises:

        HTTPException: If the credentials are incorrect (401 Unauthorized) or the user account is inactive (403 Forbidden).
    """

    # Authenticate the user:
    user = authenticate_user(form_data.username, form_data.password)

    # Create the access_token:
    access_token = create_access_token(data={"sub": user.email}, scope="api")

    # get the expiry date time:
    expiry_date_time = (
        datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    ).strftime("%Y-%m-%d %H:%M:%S")

    # create the token object:
    token = Token()

    # set the access token, token type, expiry, expiry date time, and success status:
    token.access_token = access_token
    token.token_type = "bearer"
    token.expiry = f"{ACCESS_TOKEN_EXPIRE_DAYS} days(s)"
    token.expiry_date_time = expiry_date_time
    token.success = True

    return token


@router.get("/users", response_model=List[User], tags=["User"])
async def get_users(
    session: Session = Depends(get_session),
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
):
    query = select(User)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            or_(
                User.name.ilike(search_filter),
                User.email.ilike(search_filter),
                cast(User.active, String).ilike(search_filter),
            )
        )

    if sort_by:
        column = getattr(User, sort_by, None)
        if not column:
            raise HTTPException(status_code=400, detail="Invalid sort column")
        query = query.order_by(desc(column) if sort_order == "desc" else asc(column))

    return session.exec(query).all()


@router.get("/users/{user_id}", response_model=User, tags=["User"])
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=dict, tags=["User"])
def add_users(users: List[User], session: Session = Depends(get_session)):
    """
    To insert many users, remove the id key in the request body.
    The id key is automatically generated by the database.
    """
    for user in users:
        # Check if the user id is provided and already exists in the database.
        if user.id is not None and session.get(User, user.id):
            raise HTTPException(
                status_code=400, detail=f"User ID {user.id} already exists"
            )
        # Check if the user email already exists.
        existing_user = session.exec(
            select(User).where(User.email == user.email)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail=f"User email {user.email} already exists"
            )
        # Hash the plain-text password.
        user.password = get_password_hash(user.password)
        session.add(user)

    session.commit()

    return {"message": f"{len(users)} users added successfully"}


@router.delete("/users/{user_id}", response_model=dict, tags=["User"])
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"detail": "User deleted successfully"}


@router.put("/users/{user_id}", response_model=User, tags=["User"])
def update_user(
    user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)

    # If a new password is provided, hash it before saving
    if "password" in update_data and update_data["password"]:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    return {"detail": "User updated successfully"}
