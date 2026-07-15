from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Memo App")


class MemoCreate(BaseModel):
    """POST 요청으로 받을 메모 생성 데이터."""

    title: str = Field(min_length=1, examples=["오늘의 메모"])
    content: str = Field(min_length=1, examples=["회의 준비하기"])


class MemoUpdate(BaseModel):
    """PUT 요청으로 받을 메모 수정 데이터."""

    id: int = Field(ge=1, examples=[1])
    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용"])


memos: Dict[int, Dict[str, str]] = {}
next_memo_id = 1


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _get_memo_or_404(memo_id: int) -> Dict[str, str]:
    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memos[memo_id]


@app.get("/memos")
def list_memos():
    """전체 메모를 최신순으로 조회한다."""

    data = sorted(
        memos.values(),
        key=lambda memo: (memo["created_at"], memo["id"]),
        reverse=True,
    )
    return {"data": data}


@app.post("/memos", status_code=201)
def create_memo(memo: MemoCreate):
    """새 메모를 생성한다."""

    global next_memo_id

    new_memo = {
        "id": next_memo_id,
        "title": memo.title,
        "content": memo.content,
        "created_at": _now_str(),
    }
    memos[next_memo_id] = new_memo
    next_memo_id += 1

    return {"message": "memo created", "data": new_memo}


@app.put("/memos")
def update_memo(memo_id: int, memo: MemoUpdate):
    """기존 메모를 수정한다."""

    if memo.id != memo_id:
        raise HTTPException(status_code=400, detail="Memo ID mismatch")

    existing = _get_memo_or_404(memo_id)
    updated_memo = {
        "id": memo_id,
        "title": memo.title,
        "content": memo.content,
        "created_at": existing["created_at"],
    }
    memos[memo_id] = updated_memo

    return {"message": "memo updated", "data": updated_memo}


@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    """기존 메모를 삭제한다."""

    deleted = _get_memo_or_404(memo_id)
    memos.pop(memo_id)

    return {"message": "memo deleted", "data": deleted}
