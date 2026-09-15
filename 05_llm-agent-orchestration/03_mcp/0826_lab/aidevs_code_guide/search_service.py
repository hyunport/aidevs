"""통합 README 검색과 관련 코드 파일 목록 생성을 담당합니다."""

from __future__ import annotations

from config import get_settings
from database import count_chunks, search_chunks
from readme_loader import related_files


def search_readmes(query: str, query_embedding: list[float], top_k: int = 5) -> dict:
    """관련 README 여러 개와 각 README 주변의 최신 코드 파일을 찾습니다."""
    normalized = query.strip()
    if not normalized:
        raise ValueError("query는 빈 문자열일 수 없습니다.")
    if len(normalized) > 2000:
        raise ValueError("query는 2,000자 이하여야 합니다.")
    if not 1 <= top_k <= 10:
        raise ValueError("top_k는 1부터 10 사이여야 합니다.")

    settings = get_settings()
    if len(query_embedding) != settings.embedding_dimensions:
        raise ValueError(
            f"query_embedding은 {settings.embedding_dimensions}차원이어야 합니다."
        )
    indexed_count = count_chunks(settings)
    if indexed_count == 0:
        return {
            "query": normalized,
            "results": [],
            "message": "색인된 README가 없습니다. index_readmes.py를 먼저 실행하세요.",
        }

    candidates = search_chunks(
        settings,
        query_embedding,
        candidate_count=max(15, top_k * 3),
    )

    unique_results: list[dict] = []
    seen_sources: set[str] = set()
    for candidate in candidates:
        source_path = candidate["source_path"]
        if source_path in seen_sources:
            continue
        seen_sources.add(source_path)
        unique_results.append(
            {
                "readme_path": source_path,
                "score": round(candidate["score"], 4),
                "matched_chunk": candidate["chunk_index"],
                "excerpt": candidate["content"][:1200],
                "related_files": related_files(settings.aidevs_root, source_path),
            }
        )
        if len(unique_results) == top_k:
            break

    return {
        "query": normalized,
        "indexed_chunks": indexed_count,
        "results": unique_results,
    }
