from fastapi.testclient import TestClient

import app as memo_app


client = TestClient(memo_app.app)


def setup_function() -> None:
    memo_app.memos.clear()
    memo_app.next_memo_id = 1


def test_list_memos_empty():
    response = client.get("/memos")
    assert response.status_code == 200
    assert response.json() == {"data": []}


def test_create_memo():
    response = client.post(
        "/memos",
        json={"title": "Today memo", "content": "Prepare the meeting"},
    )

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["id"] == 1
    assert data["title"] == "Today memo"
    assert data["content"] == "Prepare the meeting"
    assert "created_at" in data


def test_list_memos_latest_first():
    client.post("/memos", json={"title": "First", "content": "Content 1"})
    client.post("/memos", json={"title": "Second", "content": "Content 2"})

    response = client.get("/memos")

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 2
    assert data[0]["title"] == "Second"
    assert data[1]["title"] == "First"


def test_update_memo():
    client.post("/memos", json={"title": "Original", "content": "Original content"})

    response = client.put(
        "/memos",
        json={"id": 1, "title": "Updated", "content": "Updated content"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == 1
    assert data["title"] == "Updated"
    assert data["content"] == "Updated content"


def test_delete_memo():
    client.post("/memos", json={"title": "Delete", "content": "Delete content"})

    response = client.delete("/memos/1")

    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Delete"

