from typing import AsyncGenerator, Generic, List, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.mysql import mysql_database

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with mysql_database.get_session() as session:
            yield session

    async def find_one(self, statement) -> List[T]:
        async with mysql_database.get_session() as session:
            result = await session.execute(statement)
            return result.scalars().first()

    async def find_many(self, statement) -> List[T]:
        async with mysql_database.get_session() as session:
            result = await session.execute(statement)
            return result.scalars().all()

    # --- with model --- #
    async def find_by_id(self, id: int | str):
        async with mysql_database.get_session() as session:
            result = await session.get(self.model, id)

            return result

    async def find_all(self) -> List[T]:
        async with mysql_database.get_session() as session:
            result = await session.execute(select(self.model))

            return result.scalars().all()

    async def create(self, data: T):
        async with mysql_database.get_session() as session:
            session.add(data)
            await session.commit()
            await session.refresh(data)

            return data

    async def update(self, id: int, new_data: T):
        async with mysql_database.get_session() as session:
            data = await session.get(self.model, id)
            if data is None:
                return None

            for key, value in new_data.__dict__.items():
                setattr(data, key, value)

            await session.commit()
            await session.refresh(data)

            return data

    async def delete(self, instance: T) -> bool:
        async with mysql_database.get_session() as session:
            await session.delete(instance)
            await session.commit()

            return instance
