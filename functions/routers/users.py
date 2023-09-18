from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from models import NewUser, PublicUser, User, UserInDB
from utils.authentication import get_current_active_user, get_password_hash
from utils.constants import database

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    summary="Get the current user's information.",
    description=(
        "Get the current user's information from the database."
        "This endpoint requires authentication."
    ),
)
@version(1)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    return current_user


@router.get(
    "", summary="Get all users.", description="Get all users from the database."
)
@version(1)
async def read_users(page: int = 0, limit: int = 100) -> list[PublicUser]:
    """Get all users from the database."""
    return [
        PublicUser(**user)
        for user in await database.get_all_users(page=page, limit=limit)
    ]


@router.post(
    "/register",
    summary="Register a new user.",
    description="Register a new user.",
)
@version(1)
async def register_user(data: NewUser) -> User:
    """Register a new user."""
    user = UserInDB(**data.dict(), hashed_password=get_password_hash(data.password))
    return await database.create_user(user)
