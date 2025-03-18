import asyncio
from functools import partial

import pytest
from httpx import ASGITransport, AsyncClient

from src.databases.mysql import mysql_database
from src.main import app
from src.tests.containers.mysql_container import MysqlContainer


@pytest.fixture(scope="session", autouse=True)
async def mysql_container():
    mysql_container = MysqlContainer(image="mysql:8.0")
    await mysql_container.open_database()
    await mysql_container.check_connect_database()

    yield mysql_container

    await mysql_container.close_database()


@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown_models(mysql_container: MysqlContainer):
    await mysql_container.setup_models()
    yield
    await mysql_container.teardown_models()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def mock_mysql_client(mysql_container: MysqlContainer):
    mysql_database.get_session = partial(mysql_container.get_session)


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
