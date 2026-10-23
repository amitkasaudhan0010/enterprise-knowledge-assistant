from app.models.document import DocumentChunk
from app.services.retrieval import LocalFaissRetriever


def test_empty_index_returns_no_results() -> None:
    retriever = LocalFaissRetriever()

    assert retriever.search("What is RAG?") == []


def test_empty_query_is_rejected() -> None:
    retriever = LocalFaissRetriever()

    try:
        retriever.search("   ")
        assert False, "Expected ValueError"
    except ValueError:
        pass