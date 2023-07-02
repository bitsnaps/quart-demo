import pytest
from src.main import app, TodoIn

@pytest.mark.asyncio
async def test_echo() -> None:
    test_client = app.test_client()
    response = await test_client.post("/echo", json={"a": "b"})
    data = await response.get_json()
    assert data == {"extra":True,"input":{"a":"b"}}

@pytest.mark.asyncio
async def test_create_todo() -> None:
    test_client = app.test_client()
    response = await test_client.post("/todos/", json=TodoIn(task="Abc", due=None))
    data = await response.get_json()
    assert data == {"id": 1, "task": "Abc", "due": None}
