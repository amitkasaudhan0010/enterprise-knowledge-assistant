import pytest

from app.services.chunking import split_into_chunks


def test_chunks_preserve_metadata() -> None:
    result = split_into_chunks(
        text="Python helps build AI applications.",
        document_id="doc-001",
        source="guide.txt",
        chunk_size=3,
        overlap=1,
    )

    assert len(result) == 2
    assert result[0].document_id == "doc-001"
    assert result[0].source == "guide.txt"
    assert result[0].chunk_index == 0
    assert result[1].chunk_index == 1


def test_invalid_overlap_raises_error() -> None:
    with pytest.raises(ValueError):
        split_into_chunks(
            text="some words",
            document_id="doc-001",
            source="guide.txt",
            chunk_size=5,
            overlap=5,
        )


def test_empty_text_returns_no_chunks() -> None:
    result = split_into_chunks(
        text="",
        document_id="doc-001",
        source="guide.txt",
    )

    assert result == []