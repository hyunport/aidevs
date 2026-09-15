"""프로젝트 경로와 환경 변수를 한곳에서 관리합니다."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parent
COURSE_DIR = PROJECT_DIR.parents[2]
DEFAULT_AIDEVS_ROOT = PROJECT_DIR.parents[3]

load_dotenv(COURSE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    aidevs_root: Path
    database_url: str
    openai_api_key: str
    openai_model: str
    embedding_model: str
    embedding_dimensions: int
    chunk_size: int
    chunk_overlap: int


def get_settings(*, require_api_key: bool = True) -> Settings:
    """환경 변수를 검증하고 타입이 정리된 설정을 반환합니다."""
    root = Path(os.getenv("AIDEVS_ROOT", str(DEFAULT_AIDEVS_ROOT))).resolve()
    database_url = os.getenv("DATABASE_URL", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not root.is_dir():
        raise RuntimeError(f"AIDEVS_ROOT 폴더를 찾을 수 없습니다: {root}")
    if not database_url:
        raise RuntimeError("05_llm-agent-orchestration/.env에 DATABASE_URL이 필요합니다.")
    if require_api_key and not api_key:
        raise RuntimeError("05_llm-agent-orchestration/.env에 OPENAI_API_KEY가 필요합니다.")

    return Settings(
        aidevs_root=root,
        database_url=database_url,
        openai_api_key=api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        embedding_model=os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
        embedding_dimensions=int(os.getenv("OPENAI_EMBEDDING_DIMENSIONS", "1536")),
        chunk_size=int(os.getenv("README_CHUNK_SIZE", "2400")),
        chunk_overlap=int(os.getenv("README_CHUNK_OVERLAP", "240")),
    )
