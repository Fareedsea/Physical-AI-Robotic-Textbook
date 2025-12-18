"""
Updated Content search API endpoints for the Physical AI & Humanoid Robotics Textbook
Uses Qdrant for vector storage
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import time

from rag.qdrant_store import QdrantTextbookStore

logger = logging.getLogger(__name__)
router = APIRouter()

# Global Qdrant store instance
qdrant_store: Optional[QdrantTextbookStore] = None


class ContentSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Search query for textbook content")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters for search")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results to return")
    min_relevance: float = Field(0.0, ge=0.0, le=1.0, description="Minimum relevance threshold")


class ContentSearchResult(BaseModel):
    id: str = Field(..., description="Unique identifier for the content")
    title: str = Field(..., description="Title of the content")
    content_snippet: str = Field(..., description="Snippet of the content")
    chapter: str = Field(..., description="Chapter where the content is located")
    section: Optional[str] = Field(None, description="Section within the chapter")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score to the query")
    source_url: str = Field(..., description="URL to the full content")


class ContentSearchResponse(BaseModel):
    results: List[ContentSearchResult] = Field(..., description="List of search results")
    total_count: int = Field(..., description="Total number of results found")
    query_id: str = Field(..., description="Unique identifier for this query")
    execution_time: float = Field(..., description="Time taken to execute the search in milliseconds")


@router.on_event("startup")
async def startup_event():
    """Initialize the Qdrant store on startup"""
    global qdrant_store
    try:
        # Initialize the Qdrant store
        qdrant_store = QdrantTextbookStore()
        logger.info("Qdrant store initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant store: {str(e)}")
        qdrant_store = None


@router.post("/search", response_model=ContentSearchResponse)
async def search_content(request: ContentSearchRequest):
    """
    Search textbook content based on the query using vector similarity in Qdrant
    """
    global qdrant_store

    if not qdrant_store:
        # Fallback to mock results if Qdrant store not available
        logger.warning("Qdrant store not available, returning mock results")
        return ContentSearchResponse(
            results=[
                ContentSearchResult(
                    id="mock_1",
                    title="Introduction to Physical AI",
                    content_snippet="Physical AI combines robotics and artificial intelligence...",
                    chapter="Chapter 1",
                    section="Introduction",
                    similarity_score=0.8,
                    source_url="/docs/chapter-1-basics-physical-ai/intro"
                )
            ],
            total_count=1,
            query_id="mock_query",
            execution_time=0.0
        )

    try:
        start_time = time.time()

        # Perform similarity search using Qdrant
        results = qdrant_store.search(
            query=request.query,
            k=request.max_results,
            min_relevance=request.min_relevance
        )

        # Format results
        formatted_results = []
        for doc_info, score in results:
            metadata = doc_info['metadata']
            result = ContentSearchResult(
                id=doc_info['id'],
                title=metadata.get('title', 'Untitled'),
                content_snippet=metadata.get('content', '')[:200] + "..." if len(metadata.get('content', '')) > 200 else metadata.get('content', ''),
                chapter=metadata.get('chapter', 'Unknown'),
                section=metadata.get('section', ''),
                similarity_score=score,
                source_url=metadata.get('relative_path', '').replace('\\', '/').replace('.md', '')
            )
            formatted_results.append(result)

        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return ContentSearchResponse(
            results=formatted_results,
            total_count=len(formatted_results),
            query_id=f"search_{hash(request.query) % 1000000}",
            execution_time=execution_time
        )

    except Exception as e:
        logger.error(f"Error performing content search: {str(e)}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Error performing content search")


@router.get("/search", response_model=ContentSearchResponse)
async def search_content_get(
    query: str = Query(..., min_length=1, max_length=1000, description="Search query for textbook content"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results to return"),
    min_relevance: float = Query(0.0, ge=0.0, le=1.0, description="Minimum relevance threshold")
):
    """
    Search textbook content using GET method (for simpler integration)
    """
    request = ContentSearchRequest(
        query=query,
        max_results=max_results,
        min_relevance=min_relevance
    )
    return await search_content(request)