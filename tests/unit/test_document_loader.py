from pathlib import Path

import pytest

from app.services.document_loader import load_document


def test_load_txt_file(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "Hello AI\n\nWelcome to RAG.",
        encoding="utf-8",
    )

    result = load_document(file_path)

    assert result == "Hello AI\nWelcome to RAG."


def test_unsupported_file_type(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.csv"
    file_path.write_text("a,b", encoding="utf-8")

    with pytest.raises(ValueError):
        load_document(file_path)


def test_empty_text_file_fails(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        load_document(file_path)