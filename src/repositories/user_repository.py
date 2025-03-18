from sqlalchemy import select

from src.models.user_model import UserModel
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self):
        super().__init__(UserModel)

    async def find_users_by_age_range(self, min_age: int, max_age: int):
        statement = select(UserModel).where(UserModel.age >= min_age, UserModel.age <= max_age)
        return await self.find_many(statement=statement)

    async def find_users_by_name(self, name: str):
        statement = select(UserModel).where(UserModel.name.like(f"%{name}%"))
        return await self.find_many(statement=statement)
