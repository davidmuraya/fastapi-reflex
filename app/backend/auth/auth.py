from datetime import datetime, timedelta
from urllib.parse import unquote

import jose
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.backend.auth.models import TokenData, User
from app.backend.database.utils import get_engine

APP_SECRET_KEY = "d04b8796215899e3a64fbf7751d2d3cef000a1bbc30f70a9904219b82c3e3fe207"
API_SECRET_KEY = "1MFKsQ75FiCNNwX5jkf6LF999baV1L6eFN3jKCnyGmZ_M"

ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 3200
ACCESS_TOKEN_EXPIRE_DAYS = 10

# set the password hashing context:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# set the OAuth2 scheme:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")


# Authentication used by the HTML App:
def get_current_app_user(access_token: str = Cookie(None)):
    # check if the access token is present:
    if not access_token:
        return None
    else:
        # URL-decode the access token to convert any '%20' back to a space.
        access_token = unquote(access_token)

        # Split the access token into the scheme and the payload.
        scheme, _, param = access_token.partition(" ")
        try:
            payload = jwt.decode(param, APP_SECRET_KEY, algorithms=ALGORITHM)

            #  get the email from the payload
            email = payload.get("sub")

            #  get the user from the database
            user = get_user(email=email)
        except jose.ExpiredSignatureError as e:
            print(e)
            return None
        except jose.exceptions.JWTError as e:
            print(f"Signature verification failed. {e}")
            return None

    return user


# Function to retrieve a user by email
def get_user(email: str) -> User | None:
    # Get the user from the database
    engine = get_engine()
    with Session(engine) as session:
        db_user = session.exec(select(User).where(User.email == email)).first()

        return db_user


# Function to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    username_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Couldn't find email in payload.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Couldn't find user. Please check on your email and password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    jwt_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please check on the token and its validity. It may have expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise username_credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise jwt_credentials_exception

    user = get_user(email=token_data.email)

    if user is None:
        raise user_credentials_exception

    return user


# Function to authenticate a user by checking their username and password
def authenticate_user(email: str, password: str):
    """
    Authenticate a user by checking their username and password.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The password provided by the user.

    Raises:
        HTTPException: Raises HTTP 404 Not Found status if username not found.
        HTTPException: Raises HTTP 400 Bad Request status if incorrect credentials.
    """
    # Exceptions:
    username_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Username not found. Please check on your email, or sign-up.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    incorrect_credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username or password. Please check on your username and password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # get the user details:
    user = get_user(email=email)

    # check if the user exists:
    if not user:
        raise username_not_found_exception

    # check if the password is correct:
    if not verify_password(password, user.password):
        raise incorrect_credentials_exception

    return user


# Function to get the current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # Exceptions:
    inactive_user_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Inactive User. User Account has not been activated.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # check if the user is active:
    if not current_user.active:
        raise inactive_user_exception
    return current_user


# function to create an access token:
def create_access_token(
    data: dict,
    scope: str,
    expires_delta: timedelta = None,
):
    to_encode = data.copy()

    # get the current time:
    now = datetime.utcnow()

    # expire the token after the expires delta:
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    # set the scope of the token:
    if scope == "app":
        SECRET_KEY = APP_SECRET_KEY
    elif scope == "api":
        SECRET_KEY = API_SECRET_KEY

    # set expiry, and the nbf (not before) to the current time:
    to_encode.update({"exp": expire, "nbf": now})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# function to verify the password:
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# function to get the password hash:
def get_password_hash(password):
    return pwd_context.hash(password)
