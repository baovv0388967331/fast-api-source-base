import pytest


@pytest.mark.asyncio
async def test_create_item(async_client):
    response = await async_client.post("/users", json={"name": "Test Item", "age": 1})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["age"] == 1
    assert "id" in data


@pytest.mark.asyncio
async def test_read_item(async_client):
    response = await async_client.post("/users", json={"name": "Test Item", "age": 1})
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    response = await async_client.get(f"/users/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["age"] == 1
    assert data["id"] == item_id


@pytest.mark.asyncio
async def test_update_item(async_client):
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


@pytest.mark.asyncio
async def test_delete_item(async_client):
    item_id = 1
    response = await async_client.delete(f"/users/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == item_id
    # response = await async_client.get(f"/users/{item_id}")
    # assert response.status_code == 404, response.text
