from pydantic import BaseModel
from typing import List, Optional
import uuid

class Document(BaseModel):
    id: str = str(uuid.uuid4())
    content: str
    metadata: dict = {}

class IngestRequest(BaseModel):
    text: str
    source_id: str
    metadata: Optional[dict] = {}

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Simple overlapping chunk strategy.
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    
    return chunks

from rag.embeddings import get_embedding
from db.qdrant import upsert_vectors, init_collection
from qdrant_client.http import models
import uuid

# Ensure collection exists on startup or first run
COLLECTION_NAME = "textbook_content"

async def process_ingest(request: IngestRequest):
    """
    Processes the ingestion request:
    1. Chunks the text.
    2. Generates embeddings.
    3. Stores in Qdrant.
    """
    # Initialize implementation (idempotent)
    init_collection(COLLECTION_NAME)

    chunks = chunk_text(request.text)
    points = []

    for chunk in chunks:
        vector = get_embedding(chunk)
        if not vector:
            continue
            
        point_id = str(uuid.uuid4())
        payload = {
            "content": chunk,
            "source_id": request.source_id,
            **request.metadata
        }
        
        points.append(models.PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        ))

    if points:
        upsert_vectors(COLLECTION_NAME, points)
    
    return {
        "status": "success",
        "chunks_processed": len(chunks),
        "vectors_stored": len(points),
        "document_id": request.source_id
    }
