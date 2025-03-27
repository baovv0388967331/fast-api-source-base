from functools import partial

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.databases.mysql import mysql_database
from src.main import app
from src.tests.containers.mysql_container import MysqlContainer


@pytest_asyncio.fixture(scope="session")
async def mysql_container():
    container = MysqlContainer()
    await container.check_connect_database()
    await container.setup_models()

    yield container

    await container.teardown_models()
    await container.close_database()


@pytest_asyncio.fixture(scope="function")
async def async_client(mysql_container: MysqlContainer):
    mysql_database.get_session = partial(mysql_container.get_session)
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
