from abc import ABC, abstractmethod
from typing import Any

from models.user import User, UserInDB


class Database(ABC):
    @abstractmethod
    async def get_by_username(self, key: str) -> dict[str, Any] | None:
        ...

    @abstractmethod
    async def get_all_users(
        self, page: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def connect(self) -> None:
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        ...

    @abstractmethod
    async def create_user(self, user: UserInDB) -> User:
        ...
