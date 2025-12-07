from rag.embeddings import get_embedding
from db.qdrant import search_vectors, COLLECTION_NAME

def retrieve_context(query: str, limit: int = 3) -> list[str]:
    """
    Retrieves relevant text chunks for a given query.
    """
    vector = get_embedding(query)
    if not vector:
        return []

    results = search_vectors(COLLECTION_NAME, vector, limit=limit)
    
    contexts = []
    for hit in results:
        contexts.append(hit.payload.get("content", ""))
    
    return contexts
