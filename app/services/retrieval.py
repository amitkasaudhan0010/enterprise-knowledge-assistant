import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.models.document import DocumentChunk


class LocalFaissRetriever:
    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.index = None
        self.chunks: list[DocumentChunk] = []

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        if not chunks:
            return

        texts = [chunk.text for chunk in chunks]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")

        if self.index is None:
            dimension = vectors.shape[1]
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)
        self.chunks.extend(chunks)

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be positive.")

        if self.index is None or not self.chunks:
            return []

        query_vector = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")

        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_vector, k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "chunk": self.chunks[int(index)].model_dump(),
                }
            )

        return results