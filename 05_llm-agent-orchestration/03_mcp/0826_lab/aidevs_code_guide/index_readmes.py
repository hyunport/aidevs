"""AIDEVS 전체 README를 OpenAI Embedding으로 pgvector에 색인합니다."""

from __future__ import annotations

import argparse

from openai import OpenAI

from config import get_settings
from database import apply_index_changes, count_chunks, fetch_index_state
from readme_loader import load_readme_chunks


def batched(items: list, size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def index_readmes(*, dry_run: bool = False, batch_size: int = 64) -> dict:
    settings = get_settings(require_api_key=not dry_run)
    chunks = load_readme_chunks(
        settings.aidevs_root,
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap,
    )
    state = fetch_index_state(settings)
    changed_chunks = [
        chunk for chunk in chunks if state.get(chunk.id) != chunk.content_hash
    ]
    current_ids = {chunk.id for chunk in chunks}
    stale_count = len(set(state) - current_ids)

    summary = {
        "readme_chunks": len(chunks),
        "changed_chunks": len(changed_chunks),
        "unchanged_chunks": len(chunks) - len(changed_chunks),
        "stale_chunks": stale_count,
        "embedding_model": settings.embedding_model,
        "dry_run": dry_run,
    }
    if dry_run:
        return summary

    client = OpenAI(api_key=settings.openai_api_key)
    embedded: list[tuple] = []
    total_tokens = 0
    for group in batched(changed_chunks, batch_size):
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=[chunk.content for chunk in group],
            dimensions=settings.embedding_dimensions,
        )
        total_tokens += response.usage.total_tokens
        vectors = sorted(response.data, key=lambda item: item.index)
        embedded.extend(
            (chunk, vector.embedding) for chunk, vector in zip(group, vectors, strict=True)
        )

    updated, deleted = apply_index_changes(settings, embedded, current_ids)
    summary.update(
        {
            "updated_chunks": updated,
            "deleted_chunks": deleted,
            "total_embedding_tokens": total_tokens,
            "database_chunks": count_chunks(settings),
        }
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="AIDEVS README pgvector 색인")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="API를 호출하지 않고 변경될 Chunk 수만 확인합니다.",
    )
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()
    result = index_readmes(dry_run=args.dry_run, batch_size=args.batch_size)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
