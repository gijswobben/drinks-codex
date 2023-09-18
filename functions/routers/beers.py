import uuid
from typing import Annotated

from exceptions import (
    admin_required_exception,
    beer_already_exists_exception,
    beer_not_found_exception,
)
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_versioning import version
from models.beer import Beer, NewBeer
from models.user import User
from utils.authentication import get_current_active_user
from utils.constants import database

router = APIRouter(prefix="/beers", tags=["Beers"])


@router.get(
    "",
    summary="Get all beers.",
    description="Get all beers from the database.",
)
@version(1)
async def read_beers(page: int = 0, limit: int = 100) -> list[Beer]:
    """Get all beers from the database."""
    return [
        Beer(**beer) for beer in await database.get_all_beers(page=page, limit=limit)
    ]


@router.get(
    "/{beer_id}",
    summary="Get a beer by ID.",
    description="Get a beer from the database by its ID.",
)
@version(1)
async def read_beer(beer_id: str) -> Beer:
    """Get a beer from the database by its ID."""
    beer = await database.get_beer_by_id(beer_id)
    if beer is None:
        raise beer_not_found_exception
    return Beer(**beer)


@router.post(
    "",
    summary="Create a beer.",
    description="Create a beer in the database.",
)
@version(1)
async def create_beer(
    beer: NewBeer, current_user: Annotated[User, Depends(get_current_active_user)]
) -> Beer:
    """Create a beer in the database."""
    if not current_user.is_admin:
        raise admin_required_exception
    beer_uuid = str(uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=beer.name))
    if await database.get_beer_by_id(beer_uuid) is not None:
        raise beer_already_exists_exception
    return Beer(**(await database.create_beer({**beer.dict(), "uuid": beer_uuid})))


@router.delete(
    "/{beer_id}",
    summary="Delete a beer by ID.",
    description="Delete a beer from the database by its ID.",
)
@version(1)
async def delete_beer(
    beer_id: str, current_user: Annotated[User, Depends(get_current_active_user)]
) -> None:
    """Delete a beer from the database by its ID."""
    if not current_user.is_admin:
        raise admin_required_exception
    if await database.get_beer_by_id(beer_id) is None:
        raise beer_not_found_exception
    await database.delete_beer_by_id(beer_id)
