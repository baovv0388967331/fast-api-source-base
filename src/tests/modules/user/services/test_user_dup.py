import pytest_asyncio

from src.models.user_model import UserModel
from src.tests.containers.mysql_container import MysqlContainer
from src.tests.core.async_base import AsyncBase


@pytest_asyncio.fixture(scope="function")
async def setup_data(mysql_container: MysqlContainer):
    items = [UserModel(id=2, name="Test Item", age=1)]
    await AsyncBase.add_items(mysql_container, items)

    yield

    await AsyncBase.clear_data(mysql_container, UserModel)


class TestUserApi:
    async def test_read_item(self, async_client, setup_data):
        item_id = 2
        response = await async_client.get(f"/users/{item_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["age"] == 1
        assert data["id"] == item_id
