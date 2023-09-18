from typing import Any

from models.user import User, UserInDB

from db.base import Database

_dummy_db: dict[str, dict[str, Any]] = {
    "users": {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
            "is_admin": False,
        }
    },
    "beers": {},
}


class DummyUserDatabase(Database):
    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def _get_all(
        self, collection: str, page: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        all = list(_dummy_db[collection].values())
        return all[page * limit : page * limit + limit]

    # Beers

    async def get_all_beers(
        self, page: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        return await self._get_all("beers", page, limit)

    async def get_beer_by_id(self, key: str) -> dict[str, Any] | None:
        return _dummy_db["beers"].get(key, None)

    async def create_beer(self, beer: dict[str, Any]) -> dict[str, Any]:
        _dummy_db["beers"][beer["uuid"]] = beer
        return beer

    async def delete_beer_by_id(self, key: str) -> None:
        del _dummy_db["beers"][key]

    # Users

    async def get_all_users(
        self, page: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        return await self._get_all("users", page, limit)

    async def get_by_username(self, key: str) -> dict[str, Any] | None:
        return _dummy_db["users"].get(key, None)

    async def create_user(self, user: UserInDB) -> User:
        existing_user = await self.get_by_username(user.username)
        if existing_user is not None:
            raise Exception("User already exists")
        _dummy_db["users"][user.username] = user.dict()
        return User(**user.dict())
