from typing import Generic, List, Type, TypeVar

from sqlalchemy import select

from src.databases.mysql import mysql_database

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_session(self):
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
            return await session.get(self.model, id)

    async def find_all(self) -> List[T]:
        async with mysql_database.get_session() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def create(self, data: T):
        async with mysql_database.get_session() as session:
            try:
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return data
            except Exception:
                await session.rollback()
                return None

    async def update(self, id: int, new_data: T):
        async with mysql_database.get_session() as session:
            try:
                data = await session.get(self.model, id)
                if data is None:
                    return None

                for key, value in new_data.__dict__.items():
                    setattr(data, key, value)

                await session.commit()
                await session.refresh(data)
                return data
            except Exception:
                await session.rollback()
                return None

    async def delete(self, instance: T) -> bool:
        async with mysql_database.get_session() as session:
            try:
                await session.delete(instance)
                await session.commit()
                return True
            except Exception:
                await session.rollback()
                return False
