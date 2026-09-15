"""Markdown 포트폴리오 문서를 Ollama로 Embedding하여 pgvector에 저장합니다."""

from pathlib import Path

from _pgvector_store import delete_collection, ensure_schema, similarity_search, upsert_text


ROOT = Path(__file__).resolve().parent
DOCUMENT_DIR = ROOT / "documents"
COLLECTION = "portfolio_demo"

DOCUMENTS = [
    (
        "태웅님 포트폴리오",
        "portfolio-taewoong.md",
        {"document_type": "portfolio", "user_id": "user_001", "user_name": "태웅"},
    ),
    (
        "오현님 포트폴리오",
        "portfolio-ohyeon.md",
        {"document_type": "portfolio", "user_id": "user_002", "user_name": "오현"},
    ),
    (
        "기화님 포트폴리오",
        "portfolio-gihwa.md",
        {"document_type": "portfolio", "user_id": "user_003", "user_name": "기화"},
    ),
    (
        "투자 성향 분류 기준",
        "investment-profile-guide.md",
        {"document_type": "guide", "guide_type": "profile"},
    ),
    (
        "포트폴리오 위험 분석 기준",
        "portfolio-risk-guide.md",
        {"document_type": "guide", "guide_type": "risk"},
    ),
    (
        "균형형 목표 포트폴리오",
        "balanced-portfolio-guide.md",
        {"document_type": "guide", "guide_type": "balanced_target"},
    ),
]


def index_documents() -> None:
    ensure_schema()
    delete_collection(COLLECTION)

    for chunk_index, (title, filename, metadata) in enumerate(DOCUMENTS):
        path = DOCUMENT_DIR / filename
        content = path.read_text(encoding="utf-8")
        upsert_text(
            collection=COLLECTION,
            title=title,
            content=content,
            source=f"documents/{filename}",
            chunk_index=chunk_index,
            metadata=metadata,
        )
        print(f"저장: {filename}")


if __name__ == "__main__":
    index_documents()

    question = "태웅님의 포트폴리오와 주요 위험을 알려줘."
    print("\n질문:", question)
    for item in similarity_search(question, collection=COLLECTION, top_k=5):
        print(f"{item['score']:.3f} | {item['source']} | {item['title']}")

