# import asyncio
from functools import partial

import pytest
from httpx import ASGITransport, AsyncClient

from src.databases.mysql import mysql_database
from src.main import app
from src.tests.containers.mysql_container import MysqlContainer

# @pytest.fixture(scope="session", autouse=True)
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
async def mysql_container():
    mysql_container = MysqlContainer()
    await mysql_container.open_database()
    await mysql_container.check_connect_database()
    await mysql_container.setup_models()

    yield mysql_container

    await mysql_container.teardown_models()
    await mysql_container.close_database()


@pytest.fixture
async def async_client(mysql_container: MysqlContainer):
    mysql_database.get_session = partial(mysql_container.get_session)
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
