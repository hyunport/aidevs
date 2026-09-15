"""README 발견, Chunk 분리, 주변 코드 파일 탐색을 담당합니다."""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

RELATED_EXTENSIONS = {
    ".py",
    ".ps1",
    ".sql",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class ReadmeChunk:
    id: str
    source_path: str
    chunk_index: int
    content: str
    content_hash: str


def discover_readmes(root: Path) -> list[Path]:
    """제외 폴더를 건너뛰며 모든 README.md를 찾습니다."""
    found: list[Path] = []
    for current, dirnames, filenames in os.walk(root, topdown=True, onerror=lambda _: None):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for name in filenames:
            if name.lower() == "readme.md":
                found.append(Path(current) / name)
    return sorted(found, key=lambda path: path.as_posix().lower())


def _split_long_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    parts: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        parts.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return [part for part in parts if part]


def chunk_markdown(text: str, chunk_size: int = 2400, overlap: int = 240) -> list[str]:
    """Markdown 문단 경계를 우선 보존하여 검색용 Chunk로 나눕니다."""
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    blocks = [block.strip() for block in re.split(r"\n\s*\n", normalized) if block.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_length = 0

    for block in blocks:
        if len(block) > chunk_size:
            if current:
                chunks.append("\n\n".join(current))
                current = []
                current_length = 0
            chunks.extend(_split_long_text(block, chunk_size, overlap))
            continue

        added_length = len(block) + (2 if current else 0)
        if current and current_length + added_length > chunk_size:
            previous = "\n\n".join(current)
            chunks.append(previous)
            carry = previous[-overlap:].strip() if overlap else ""
            current = [carry, block] if carry else [block]
            current_length = sum(len(item) for item in current) + 2 * (len(current) - 1)
        else:
            current.append(block)
            current_length += added_length

    if current:
        chunks.append("\n\n".join(current))
    return chunks


def load_readme_chunks(
    root: Path,
    *,
    chunk_size: int = 2400,
    overlap: int = 240,
) -> list[ReadmeChunk]:
    """모든 README를 읽고 결정적인 ID가 있는 Chunk 목록을 만듭니다."""
    records: list[ReadmeChunk] = []
    for path in discover_readmes(root):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        source_path = path.relative_to(root).as_posix()
        for index, content in enumerate(chunk_markdown(text, chunk_size, overlap)):
            record_id = hashlib.sha256(f"{source_path}:{index}".encode()).hexdigest()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            records.append(
                ReadmeChunk(
                    id=record_id,
                    source_path=source_path,
                    chunk_index=index,
                    content=content,
                    content_hash=content_hash,
                )
            )
    return records


def related_files(root: Path, source_path: str, limit: int = 20) -> list[str]:
    """README와 같은 폴더 및 바로 아래 폴더의 현재 코드 파일을 반환합니다."""
    readme_path = (root / source_path).resolve()
    if not readme_path.is_relative_to(root.resolve()) or not readme_path.is_file():
        return []

    candidates: set[Path] = set()
    for pattern in ("*", "*/*"):
        for path in readme_path.parent.glob(pattern):
            if (
                path.is_file()
                and path.suffix.lower() in RELATED_EXTENSIONS
                and path.name.lower() != "readme.md"
            ):
                resolved = path.resolve()
                if resolved.is_relative_to(root.resolve()):
                    candidates.add(resolved)

    ordered = sorted(candidates, key=lambda path: path.as_posix().lower())
    return [path.relative_to(root).as_posix() for path in ordered[:limit]]
