import pytest

pytestmark = pytest.mark.anyio


async def test_create_and_list_users(client):
    # create
    res = await client.post(
        "/users",
        json={"email": "alice@example.com", "full_name": "Alice", "password": "password123"},
    )
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice"
    assert "id" in data

    # list
    res = await client.get("/users")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1
