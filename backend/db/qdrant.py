import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# If no credentials provided, fallback to local memory for development/testing
if not QDRANT_URL:
    print("WARNING: QDRANT_URL not set. Using in-memory storage.")
    qdrant_client = QdrantClient(":memory:")
else:
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

def get_qdrant_client():
    return qdrant_client

def init_collection(collection_name: str, vector_size: int = 1536):
    """
    Ensures the collection exists. 
    1536 is the dimension for text-embedding-3-small (OpenAI).
    """
    from qdrant_client.http import models
    
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def upsert_vectors(collection_name: str, points: list):
    """
    Upserts points into the specified collection.
    Points should be a list of models.PointStruct
    """
    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Upserted {len(points)} points into {collection_name}")
    except Exception as e:
        print(f"Error upserting vectors: {e}")

def search_vectors(collection_name: str, query_vector: list, limit: int = 5):
    """
    Searches the collection for the nearest neighbors.
    """
    try:
        return qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
    except Exception as e:
        print(f"Error searching vectors: {e}")
        return []
