"""포트폴리오 데모용 Ollama Embedding 및 pgvector 저장소."""

import os
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

import httpx
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "embeddinggemma")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://portfolio_user:portfolio_password@127.0.0.1:5434/portfolio_db",
)


def embed(text: str) -> list[float]:
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/embed",
        json={"model": EMBEDDING_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


def connect():
    connection = psycopg.connect(DATABASE_URL)
    register_vector(connection)
    return connection


def ensure_schema() -> None:
    """포트폴리오 문서 저장에 필요한 최소 Schema를 준비합니다."""
    with psycopg.connect(DATABASE_URL, autocommit=True) as connection:
        connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id UUID PRIMARY KEY,
                collection_name TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                embedding_provider TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_dimension INTEGER NOT NULL,
                embedding VECTOR NOT NULL,
                metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS documents_collection_idx
            ON documents (collection_name, embedding_provider, embedding_model)
            """
        )


def delete_collection(collection: str) -> None:
    with connect() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM documents WHERE collection_name = %s", (collection,))


def upsert_text(
    *,
    collection: str,
    title: str,
    content: str,
    source: str,
    chunk_index: int = 0,
    metadata: dict[str, Any] | None = None,
) -> str:
    vector = embed(f"{title}\n{content}")
    document_id = uuid5(NAMESPACE_URL, f"{collection}:{source}:{chunk_index}")

    with connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO documents
                (id, collection_name, title, content, source, chunk_index,
                 embedding_provider, embedding_model, embedding_dimension,
                 embedding, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, 'ollama', %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                content = EXCLUDED.content,
                embedding_model = EXCLUDED.embedding_model,
                embedding_dimension = EXCLUDED.embedding_dimension,
                embedding = EXCLUDED.embedding,
                metadata = EXCLUDED.metadata,
                created_at = NOW()
            """,
            (
                document_id,
                collection,
                title,
                content,
                source,
                chunk_index,
                EMBEDDING_MODEL,
                len(vector),
                vector,
                Jsonb(metadata or {}),
            ),
        )
    return str(document_id)


def similarity_search(
    query: str,
    *,
    collection: str,
    top_k: int = 3,
    metadata_filter: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    if top_k < 1:
        raise ValueError("top_k는 1 이상이어야 합니다.")

    vector = embed(query)
    metadata_filter = metadata_filter or {}

    with connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, content, source, chunk_index, metadata,
                   1 - (embedding <=> %s::vector) AS score
            FROM documents
            WHERE collection_name = %s
              AND embedding_provider = 'ollama'
              AND embedding_model = %s
              AND embedding_dimension = %s
              AND (%s::jsonb = '{}'::jsonb OR metadata @> %s::jsonb)
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (
                vector,
                collection,
                EMBEDDING_MODEL,
                len(vector),
                Jsonb(metadata_filter),
                Jsonb(metadata_filter),
                vector,
                top_k,
            ),
        )
        return [
            {
                "id": str(row[0]),
                "title": row[1],
                "content": row[2],
                "source": row[3],
                "chunk_index": row[4],
                "metadata": row[5],
                "score": float(row[6]),
            }
            for row in cursor.fetchall()
        ]

