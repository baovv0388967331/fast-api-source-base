from sqlalchemy import delete

from src.tests.containers.mysql_container import MysqlContainer


class AsyncBase:
    @staticmethod
    async def add_items(mysql_container: MysqlContainer, items):
        async with mysql_container.get_session() as session:
            for item in items:
                session.add(item)
            await session.commit()

    @staticmethod
    async def clear_data(mysql_container: MysqlContainer, model):
        async with mysql_container.get_session() as session:
            await session.execute(delete(model))
            await session.commit()
