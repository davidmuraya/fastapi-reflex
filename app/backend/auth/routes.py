from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.backend.auth.auth import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    authenticate_user,
    create_access_token,
)
from app.backend.auth.models import Token, UserLoginRequest, UserLoginResponse
from app.backend.database.utils import get_session

router = APIRouter(prefix="/api/v1")


@router.post("/auth/login", response_model=UserLoginResponse)
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

    if not user:
        response_error = f"Credentials Error. Incorrect username or password. User:{form_data.username}."

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=response_error
        )

    if not user.active:
        error = (
            f"Inactive User. User Account has been disabled. User:{form_data.username}"
        )

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error)

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
