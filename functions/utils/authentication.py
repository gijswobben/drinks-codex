from datetime import datetime, timedelta
from typing import Annotated

from db.base import Database
from exceptions import inactive_user_exception, unauthorized_exception
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from jose import JWTError, jwt
from models import TokenData, User, UserInDB
from passlib.context import CryptContext

from utils.constants import ALGORITHM, SECRET_KEY, database

# Create a password context for hashing and verifying passwords
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Extract the API key (JWT token) from the request header
jwt_header = APIKeyHeader(name="Authorization", scheme_name="JWT")


async def get_user(database: Database, username: str) -> UserInDB | None:
    """Retrieve a user from the database.

    Args:
        db (Database): The database to retrieve the user from.
        username (str): The username of the user to retrieve.

    Returns:
        UserInDB | None: The user retrieved from the database, or None
            if no user was found.
    """
    user_dict = await database.get_by_username(username)
    return UserInDB(**user_dict) if user_dict is not None else None


async def authenticate_user(
    database: Database, username: str, password: str
) -> User | None:
    """Authenticate a user with a username and password.

    Args:
        db (Database): The database to retrieve the user from.
        username (str): The username of the user to retrieve.
        password (str): The password of the user to retrieve.

    Returns:
        User | None: The user retrieved from the database, or None
            if no user was found or the password was incorrect.
    """
    user = await get_user(database, username)
    if user is None:
        return None
    if not password_correct(password, user.hashed_password):
        return None
    return User(**user.dict())


def password_correct(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to check.
        hashed_password (str): The hashed password to check.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get the hash of a password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return password_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create an access token (JWT) with the given data and expiration.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None): The expiration of the token.
            Defaults to None, in which case the expiration is 15 minutes
            from now.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(jwt_header)]) -> User:
    """Get the currently authenticated user.

    Args:
        token (Annotated[str, Depends): The JWT token.

    Raises:
        credentials_exception: Raised if the token is invalid.

    Returns:
        User: The user retrieved from the database.
    """
    credentials_exception = unauthorized_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        if token_data.username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(database=database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user.dict())


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Get the currently authenticated user if they are active.

    Args:
        current_user (Annotated[User, Depends): The currently
            authenticated user.

    Raises:
        HTTPException: Raised if the user is inactive.

    Returns:
        User: The currently authenticated user.
    """
    if current_user.disabled:
        raise inactive_user_exception
    return current_user
