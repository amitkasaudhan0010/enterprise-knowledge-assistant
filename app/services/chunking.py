from app.models.document import DocumentChunk


def split_into_chunks(
    text: str,
    document_id: str,
    source: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])

        chunks.append(
            DocumentChunk(
                document_id=document_id,
                source=source,
                chunk_index=len(chunks),
                text=chunk_text,
            )
        )

        if end == len(words):
            break

        start = end - overlap

    return chunks