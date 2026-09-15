"""PostgreSQL/pgvector 저장과 유사도 검색을 담당합니다."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import psycopg
from pgvector import Vector
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from config import Settings
from readme_loader import ReadmeChunk


TABLE_NAME = "aidevs_readme_chunks"


def connect(settings: Settings) -> psycopg.Connection:
    conn = psycopg.connect(settings.database_url, connect_timeout=10)
    register_vector(conn)
    return conn


def ensure_schema(settings: Settings) -> None:
    """전용 테이블과 코사인 검색 Index를 안전하게 생성합니다."""
    with connect(settings) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id TEXT PRIMARY KEY,
                source_path TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                embedding vector({settings.embedding_dimensions}) NOT NULL,
                metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                indexed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (source_path, chunk_index)
            )
            """
        )
        conn.execute(
            f"""
            CREATE INDEX IF NOT EXISTS aidevs_readme_embedding_hnsw_idx
            ON {TABLE_NAME} USING hnsw (embedding vector_cosine_ops)
            """
        )


def fetch_index_state(settings: Settings) -> dict[str, str]:
    """현재 DB의 Chunk ID와 내용 Hash를 가져옵니다."""
    ensure_schema(settings)
    with connect(settings) as conn:
        rows = conn.execute(f"SELECT id, content_hash FROM {TABLE_NAME}").fetchall()
    return {row[0]: row[1] for row in rows}


def apply_index_changes(
    settings: Settings,
    changed: Iterable[tuple[ReadmeChunk, list[float]]],
    current_ids: set[str],
) -> tuple[int, int]:
    """변경 Chunk를 Upsert하고 더 이상 존재하지 않는 Chunk를 삭제합니다."""
    changed_rows = list(changed)
    with connect(settings) as conn:
        for chunk, embedding in changed_rows:
            conn.execute(
                f"""
                INSERT INTO {TABLE_NAME} (
                    id, source_path, chunk_index, content, content_hash,
                    embedding, metadata, indexed_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (id) DO UPDATE SET
                    source_path = EXCLUDED.source_path,
                    chunk_index = EXCLUDED.chunk_index,
                    content = EXCLUDED.content,
                    content_hash = EXCLUDED.content_hash,
                    embedding = EXCLUDED.embedding,
                    metadata = EXCLUDED.metadata,
                    indexed_at = NOW()
                """,
                (
                    chunk.id,
                    chunk.source_path,
                    chunk.chunk_index,
                    chunk.content,
                    chunk.content_hash,
                    Vector(embedding),
                    Jsonb({"kind": "readme", "source": chunk.source_path}),
                ),
            )

        existing_ids = {
            row[0] for row in conn.execute(f"SELECT id FROM {TABLE_NAME}").fetchall()
        }
        stale_ids = existing_ids - current_ids
        if stale_ids:
            conn.executemany(
                f"DELETE FROM {TABLE_NAME} WHERE id = %s",
                [(record_id,) for record_id in stale_ids],
            )
    return len(changed_rows), len(stale_ids)


def count_chunks(settings: Settings) -> int:
    ensure_schema(settings)
    with connect(settings) as conn:
        row = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()
    return int(row[0])


def search_chunks(
    settings: Settings,
    query_embedding: list[float],
    candidate_count: int,
) -> list[dict[str, Any]]:
    """코사인 유사도가 높은 README Chunk를 반환합니다."""
    ensure_schema(settings)
    query_vector = Vector(query_embedding)
    with connect(settings) as conn:
        rows = conn.execute(
            f"""
            SELECT source_path, chunk_index, content,
                   1 - (embedding <=> %s) AS score
            FROM {TABLE_NAME}
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (query_vector, query_vector, candidate_count),
        ).fetchall()
    return [
        {
            "source_path": row[0],
            "chunk_index": row[1],
            "content": row[2],
            "score": float(row[3]),
        }
        for row in rows
    ]
