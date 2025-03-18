from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.mysql import MySqlContainer

from src.models.user_model import Base


class MysqlContainer(MySqlContainer):
    _database_url: str = ""
    _engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    def __init__(self, image: str):
        super().__init__(image=image)

    async def open_database(self):
        super().start()
        self._database_url = self.get_connection_url().replace("mysql://", "mysql+aiomysql://")
        self._engine = create_async_engine(self._database_url)
        self._session_maker = async_sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
        )

    async def close_database(self):
        await self.get_engine().dispose()
        super().stop()

    async def setup_models(self):
        async with self.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown_models(self):
        async with self.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def check_connect_database(self):
        try:
            async with self.get_engine().begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("✅ Connecting test database success!")
        except SQLAlchemyError as e:
            print(f"❌ Connecting test database failed!: {e}")

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            raise Exception("❌ Database engine is not initialized")
        return self._engine

    def get_session(self) -> AsyncSession:
        if self._session_maker is None:
            raise Exception("❌ Database engine is not initialized")
        return self._session_maker()
