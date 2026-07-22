r"""learning_notes 생성 예제입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\03_supabase-db-and-auth\02_supabase-table-and-crud\01_create_learning_note.py
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from supabase_client import get_supabase


def main() -> None:
    """learning_notes 테이블에 메모 1개를 생성합니다."""

    supabase = get_supabase()

    # 현재 한국 시간을 한 번만 가져옵니다.
    korea_now = datetime.now(ZoneInfo("Asia/Seoul"))

    # 년월일시분초마이크로초 형식의 문자열 ID
    # 예: 20260721153045123456
    note_id = korea_now.strftime("%Y%m%d%H%M%S%f")

    # insert는 SQL의 INSERT INTO와 비슷합니다.
    # 딕셔너리의 key는 테이블 컬럼명과 같아야 합니다.
    result = (
        supabase.table("learning_notes")
        .insert(
            {
                "id": note_id, # "20260721001"
                "title": "제목",
                "content": "내용",
                "created_at": korea_now.isoformat() # timestamptz
            }
        )
        .execute()
    )

    if not result.data:
        raise RuntimeError("insert 결과가 비어 있습니다. learning_notes 테이블과 권한을 확인하세요.")

    # [{}] ->  1개를 입력해도 리스트 형식으로 결과 값이 나온다.
    created = result.data[0]

    print("[created note]")
    print(f"id: {created.get('id')}")
    print(f"title: {created.get('title')}")
    print(f"content: {created.get('content')}")
    # print(f"created_at: {created.get('created_at')}")
    
    # Supabase에서 반환된 UTC 시간을 한국 시간으로 변환합니다.
    created_at_utc = datetime.fromisoformat(created["created_at"])
    created_at_kst = created_at_utc.astimezone(ZoneInfo("Asia/Seoul"))
    
    print(f"created_at: {created_at_kst.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
