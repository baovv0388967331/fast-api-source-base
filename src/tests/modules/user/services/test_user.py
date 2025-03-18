import pytest

from src.models.user_model import UserModel
from src.tests.containers.mysql_container import MysqlContainer
from src.tests.core.async_base import AsyncBase


@pytest.fixture(scope="function")
async def setup_data(mysql_container: MysqlContainer):
    items = [UserModel(id=1, name="Test Item", age=1)]
    await AsyncBase.add_items(mysql_container, items)

    yield

    await AsyncBase.clear_data(mysql_container, UserModel)


class TestUserApi(AsyncBase):

    @pytest.mark.usefixtures("setup_data")
    async def test_read_item(self, async_client):
        item_id = 1
        response = await async_client.get(f"/users/{item_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["age"] == 1
        assert data["id"] == item_id

    async def test_create_item(self, async_client):
        response = await async_client.post("/users", json={"name": "Test Item", "age": 1})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["age"] == 1
        assert "id" in data

    async def test_update_item(self, async_client):
        item_id = 1
        response = await async_client.put(
            f"/users/{item_id}",
            json={"name": "Updated Item", "age": 1},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Updated Item"
        assert data["age"] == 1
        assert data["id"] == item_id

    async def test_delete_item(self, async_client):
        item_id = 1
        response = await async_client.delete(f"/users/{item_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == item_id
