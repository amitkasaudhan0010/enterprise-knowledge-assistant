from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    document_id: str
    source: str
    chunk_index: int = Field(ge=0)
    text: str = Field(min_length=1)