from datetime import timedelta
from typing import Annotated

import requests
from exceptions import unauthorized_exception
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import Token
from models.providers.github import GithubEmailData, GithubUserData
from models.user import UserInDB
from utils.authentication import authenticate_user, create_access_token, get_user
from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES, database

# Create a router for authentication related endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    summary="Get an access token.",
    description="Log in to get an access token.",
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """Log in with a username and password to get an access token
    (JWT).

    Args:
        form_data (OAuth2PasswordRequestForm, Depends): The form data
            containing the username and password.

    Returns:
        Token: The access token.
    """

    # Authenticate the user with the username and password
    user = await authenticate_user(database, form_data.username, form_data.password)

    # Handle the case where the user is not authenticated
    if user is None:
        raise unauthorized_exception

    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/github-token", summary="Swap a social login access token for a custom one."
)
async def swap_token(github_access_token: str) -> Token:
    if not github_access_token:
        raise unauthorized_exception

    # Get the profile from Github
    profile_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {github_access_token}"},
    )
    profile_response.raise_for_status()

    # Get the email addresses from Github
    email_response = requests.get(
        "https://api.github.com/user/emails",
        headers={"Authorization": f"token {github_access_token}"},
    )
    email_response.raise_for_status()
    email_addresses = [GithubEmailData(**email) for email in email_response.json()]

    # Create a user data object
    user_data = GithubUserData(
        **profile_response.json(), email_addresses=email_addresses
    )

    # Create a new user if the user doesn't exist
    user = await get_user(database, user_data.primary_email.email)
    if user is None:
        user_in_db = await database.create_user(
            user=UserInDB(
                username=user_data.primary_email.email,
                full_name=user_data.name,
                profile_picture_url=user_data.avatar_url,
                email=user_data.primary_email.email,
                disabled=False,
                email_verified=user_data.primary_email.verified,
                hashed_password=None,
            )
        )
        user = await get_user(database, user_in_db.username)
        if user is None:
            raise unauthorized_exception

    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=new_access_token, token_type="bearer")
