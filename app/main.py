from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    version="0.1.0",
    description="A production-oriented RAG application.",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}