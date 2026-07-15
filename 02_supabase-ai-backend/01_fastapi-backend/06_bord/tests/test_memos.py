from fastapi.testclient import TestClient

import app as memo_app


client = TestClient(memo_app.app)


def setup_function() -> None:
    memo_app.memos.clear()
    memo_app.next_memo_id = 1


def test_create_memo() -> None:
    response = client.post(
        "/memos",
        json={"title": "오늘 할 일", "content": "문서 작성"},
    )

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["id"] == 1
    assert data["title"] == "오늘 할 일"
    assert data["content"] == "문서 작성"
    assert "created_at" in data


def test_list_memos_latest_first() -> None:
    client.post("/memos", json={"title": "첫 번째", "content": "내용1"})
    client.post("/memos", json={"title": "두 번째", "content": "내용2"})

    response = client.get("/memos")

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 2
    assert data[0]["title"] == "두 번째"
    assert data[1]["title"] == "첫 번째"


def test_get_memo_detail() -> None:
    client.post("/memos", json={"title": "상세", "content": "확인"})

    response = client.get("/memos/1")

    assert response.status_code == 200
    assert response.json()["data"]["title"] == "상세"


def test_update_memo() -> None:
    client.post("/memos", json={"title": "원본", "content": "원본 내용"})

    response = client.put(
        "/memos/1",
        json={"title": "수정본", "content": "수정된 내용"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "수정본"
    assert data["content"] == "수정된 내용"


def test_delete_memo() -> None:
    client.post("/memos", json={"title": "삭제", "content": "삭제할 내용"})

    response = client.delete("/memos/1")

    assert response.status_code == 200
    assert response.json()["data"]["title"] == "삭제"

    not_found = client.get("/memos/1")
    assert not_found.status_code == 404

