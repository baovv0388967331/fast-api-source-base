import os
from asyncio import current_task

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base


class MysqlDatabase:
    _engine: AsyncEngine | None = None
    _scope_session: AsyncSession | None = None
    _database_url = "mysql+aiomysql://%s:%s@%s:%s/%s?charset=utf8" % (
        os.environ.get("MYSQL_USER", "fastapi_user"),
        os.environ.get("MYSQL_PASSWORD", "root"),
        os.environ.get("MYSQL_HOST", "127.0.0.1"),
        os.environ.get("MYSQL_PORT", "3306"),
        os.environ.get("MYSQL_DATABASE", "fastapi_db"),
    )

    def init_db(self):
        if self._engine:
            return

        self._engine = create_async_engine(self._database_url, pool_size=100, max_overflow=0, pool_pre_ping=False)

        session_maker = async_sessionmaker(bind=self._engine, expire_on_commit=False, autocommit=False, autoflush=False)

        self._scope_session = async_scoped_session(session_maker, scopefunc=current_task)

    def get_session(self) -> AsyncSession:
        if self._scope_session is None:
            raise Exception("❌ Database session is not initialized")
        return self._scope_session()

    async def close(self):
        if self._engine is None:
            raise Exception("❌ Database engine is not initialized")
        await self._engine.dispose()

    async def check_db_session(self):
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
                print("✅ Connecting database success!")
        except SQLAlchemyError as e:
            print(f"❌ Connecting database failed!: {e}")


mysql_database = MysqlDatabase()
Base = declarative_base()
