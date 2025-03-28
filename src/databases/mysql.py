import os

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.models.user_model import Base


class MysqlDatabase:
    _database_url = "mysql+aiomysql://%s:%s@%s:%s/%s?charset=utf8" % (
        os.environ.get("MYSQL_USER", "fastapi_user"),
        os.environ.get("MYSQL_PASSWORD", "root"),
        os.environ.get("MYSQL_HOST", "127.0.0.1"),
        os.environ.get("MYSQL_PORT", "3306"),
        os.environ.get("MYSQL_DATABASE", "fastapi_db"),
    )

    _engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    async def open_database(self):
        self._engine = create_async_engine(self._database_url)
        self._session_maker = async_sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
        )

    async def close_database(self):
        await self.get_engine().dispose()

    async def check_connect_database(self):
        try:
            async with self.get_engine().begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("✅ Connecting test database success!")
        except SQLAlchemyError as e:
            print(f"❌ Connecting test database failed!: {e}")

    async def setup_models(self):
        async with self.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown_models(self):
        async with self.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            raise Exception("❌ Database engine is not initialized")
        return self._engine

    def get_session(self) -> AsyncSession:
        if self._session_maker is None:
            raise Exception("❌ Database engine is not initialized")
        return self._session_maker()


mysql_database = MysqlDatabase()
