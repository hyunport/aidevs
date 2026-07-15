from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Memo App")


class MemoCreate(BaseModel):
    title: str = Field(min_length=1, examples=["오늘의 메모"])
    content: str = Field(min_length=1, examples=["회의 준비하기"])


class MemoUpdate(BaseModel):
    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용"])


class MemoOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: str


memos: Dict[int, Dict[str, str]] = {}
next_memo_id = 1


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _get_memo_or_404(memo_id: int) -> Dict[str, str]:
    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memos[memo_id]


@app.get("/memos")
def list_memos() -> Dict[str, List[Dict[str, str]]]:
    data = sorted(
        memos.values(),
        key=lambda memo: (memo["created_at"], memo["id"]),
        reverse=True,
    )
    return {"data": data}


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int) -> Dict[str, Dict[str, str]]:
    memo = _get_memo_or_404(memo_id)
    return {"data": memo}


@app.post("/memos", status_code=201)
def create_memo(memo: MemoCreate) -> Dict[str, Dict[str, str]]:
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


@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoUpdate) -> Dict[str, Dict[str, str]]:
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
def delete_memo(memo_id: int) -> Dict[str, Dict[str, str]]:
    deleted = _get_memo_or_404(memo_id)
    memos.pop(memo_id)
    return {"message": "memo deleted", "data": deleted}
