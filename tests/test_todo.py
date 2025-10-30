from fastapi.testclient import TestClient
from app.main import app
from app.schemas import TodoCreate

client = TestClient(app)


def test_create_todo():
    response = client.post("/todos/", json={"task": "Real DB Task"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["todo"]["task"] == "Real DB Task"
    assert data["todo"]["completed"] is False
    return data["todo"]["id"]  # возвращаем id для следующих тестов


def test_get_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(todo["task"] == "Real DB Task" for todo in data)


def test_update_todo():
    todo_id = test_create_todo()
    response = client.put(f"/todos/{todo_id}", json={"task": "Updated Task"})
    assert response.status_code == 200
    data = response.json()
    assert data["task"] == "Updated Task"


def test_toggle_todo_complete():
    todo_id = test_create_todo()
    response = client.put(f"/todos/{todo_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_delete_todo():
    todo_id = test_create_todo()
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["todo"] is None
