from pathlib import Path

from readme_loader import chunk_markdown, discover_readmes, related_files


def test_chunk_markdown_keeps_all_content() -> None:
    text = "# 제목\n\n첫 번째 설명입니다.\n\n## 기능\n\n두 번째 설명입니다."
    chunks = chunk_markdown(text, chunk_size=30, overlap=0)

    assert len(chunks) >= 2
    assert "첫 번째 설명입니다." in "\n".join(chunks)
    assert "두 번째 설명입니다." in "\n".join(chunks)


def test_discover_readmes_skips_cache(tmp_path: Path) -> None:
    (tmp_path / "course").mkdir()
    (tmp_path / "course" / "README.md").write_text("정상", encoding="utf-8")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "README.md").write_text("제외", encoding="utf-8")

    found = discover_readmes(tmp_path)

    assert found == [tmp_path / "course" / "README.md"]


def test_related_files_reads_same_and_child_folder(tmp_path: Path) -> None:
    lesson = tmp_path / "lesson"
    child = lesson / "example"
    child.mkdir(parents=True)
    (lesson / "README.md").write_text("예제", encoding="utf-8")
    (lesson / "app.py").write_text("print('app')", encoding="utf-8")
    (child / "main.py").write_text("print('main')", encoding="utf-8")
    (lesson / "image.png").write_bytes(b"not-indexed")

    result = related_files(tmp_path, "lesson/README.md")

    assert result == ["lesson/app.py", "lesson/example/main.py"]
