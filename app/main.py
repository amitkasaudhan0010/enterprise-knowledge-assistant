from functools import lru_cache
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from app.services.chunking import split_into_chunks
from app.services.document_loader import load_document
from app.services.retrieval import LocalFaissRetriever

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    version="0.2.0",
)

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@lru_cache
def get_retriever() -> LocalFaissRetriever:
    return LocalFaissRetriever()


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/documents/upload", tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
) -> dict:
    filename = Path(file.filename or "").name
    suffix = Path(filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Only PDF and TXT files are supported.",
        )

    content = await file.read(MAX_UPLOAD_BYTES + 1)

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 5 MB limit.",
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid4())
    temp_path = upload_dir / f"{document_id}{suffix}"

    try:
        temp_path.write_bytes(content)
        text = load_document(temp_path)

        chunks = split_into_chunks(
            text=text,
            document_id=document_id,
            source=filename,
        )

        if not chunks:
            raise ValueError("Document produced no chunks.")

        get_retriever().add_chunks(chunks)

        return {
            "document_id": document_id,
            "filename": filename,
            "chunks_indexed": len(chunks),
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document processing failed.",
        ) from exc

    finally:
        temp_path.unlink(missing_ok=True)


@app.get("/search", tags=["Retrieval"])
def search_documents(
    q: str = Query(min_length=1, max_length=1000),
    top_k: int = Query(default=3, ge=1, le=10),
) -> dict:
    try:
        results = get_retriever().search(q, top_k)
        return {
            "query": q,
            "results": results,
            "result_count": len(results),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc