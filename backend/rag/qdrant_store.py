"""
Qdrant vector store implementation for the Physical AI & Humanoid Robotics Textbook RAG system
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging
import uuid
try:
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer, AutoModel
    EMBEDDING_AVAILABLE = True
except ImportError:
    # Fallback to a simpler approach if sentence_transformers is not available
    EMBEDDING_AVAILABLE = False
    SentenceTransformer = None
import numpy as np

from rag.new_config import rag_config

logger = logging.getLogger(__name__)

class QdrantTextbookStore:
    """Vector store using Qdrant for textbook content"""

    def __init__(self, collection_name: Optional[str] = None):
        self.collection_name = collection_name or rag_config.qdrant_collection_name

        # Try to initialize Qdrant client
        try:
            if rag_config.qdrant_api_key:
                self.client = QdrantClient(
                    url=rag_config.qdrant_url,
                    api_key=rag_config.qdrant_api_key,
                    prefer_grpc=True
                )
            else:
                self.client = QdrantClient(url=rag_config.qdrant_url)

            # Test the connection by trying to get collection info
            try:
                self.client.get_collection(self.collection_name)
                self._qdrant_available = True
                logger.info(f"Successfully connected to Qdrant, collection '{self.collection_name}' exists")
            except:
                # Collection might not exist yet, but connection works
                self._qdrant_available = True
                logger.info(f"Successfully connected to Qdrant, collection '{self.collection_name}' will be created")
        except Exception as e:
            logger.warning(f"Qdrant connection failed: {str(e)}. Operating in mock mode.")
            self.client = None
            self._qdrant_available = False

        # Initialize embedding model if available
        if EMBEDDING_AVAILABLE:
            self.embedding_model = SentenceTransformer(rag_config.embedding_model)
            self._embedding_size = self.embedding_model.get_sentence_embedding_dimension()
        else:
            # Use a default embedding size (384 for MiniLM-based models)
            self.embedding_model = None
            self._embedding_size = 384  # Default size for MiniLM models

    def _create_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        if not self._qdrant_available:
            logger.info("Qdrant not available, skipping collection creation")
            return

        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self._embedding_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection '{self.collection_name}'")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the Qdrant collection"""
        if not documents:
            return

        if not self._qdrant_available:
            logger.warning("Qdrant not available, skipping document addition")
            return

        # Prepare points for insertion
        points = []
        for doc in documents:
            # Generate embedding for the content
            if EMBEDDING_AVAILABLE and self.embedding_model:
                embedding = self.embedding_model.encode(doc['content']).tolist()
            else:
                # Fallback: use a simple embedding (all zeros with correct dimension)
                # This will allow the system to work but with no semantic similarity
                embedding = [0.0] * self._embedding_size
                logger.warning("Using zero embeddings as embedding model is not available. Semantic search will not work properly.")

            # Create a unique ID for the point
            point_id = doc.get('id', str(uuid.uuid4()))

            # Prepare payload with metadata
            payload = {
                'content': doc['content'],
                'title': doc['metadata'].get('title', ''),
                'chapter': doc['metadata'].get('chapter', ''),
                'section': doc['metadata'].get('section', ''),
                'relative_path': doc['metadata'].get('relative_path', ''),
                'source': doc['metadata'].get('source', ''),
                **doc['metadata']  # Include all other metadata
            }

            # Create point
            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
            points.append(point)

        # Upload points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        logger.info(f"Added {len(documents)} documents to Qdrant collection '{self.collection_name}'")

    def search(self, query: str, k: int = None, min_relevance: float = None) -> List[Tuple[Dict[str, Any], float]]:
        """Search for similar documents to the query"""
        k = k or rag_config.search_top_k
        min_relevance = min_relevance or rag_config.min_relevance_score

        if not self._qdrant_available:
            # Return empty results when Qdrant is not available
            logger.warning("Qdrant not available, returning empty search results")
            return []

        # Generate embedding for the query
        if EMBEDDING_AVAILABLE and self.embedding_model:
            query_embedding = self.embedding_model.encode(query).tolist()
        else:
            # Fallback: use a simple embedding (all zeros with correct dimension)
            # This will return documents but without semantic similarity
            query_embedding = [0.0] * self._embedding_size
            logger.warning("Using zero embedding for query as embedding model is not available. Search will return random results.")

        # Perform search in Qdrant
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=k,
                score_threshold=min_relevance
            )
        except AttributeError as e:
            logger.error(f"Qdrant client attribute error: {e}")
            return []
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            return []

        # Format results
        formatted_results = []
        for result in results:
            doc_info = {
                'id': result.id,
                'metadata': result.payload,
                'content': result.payload.get('content', '')
            }
            formatted_results.append((doc_info, float(result.score)))

        return formatted_results

    def search_with_selected_text(self, query: str, selected_text: str, k: int = None) -> List[Tuple[Dict[str, Any], float]]:
        """Search using both query and selected text as context"""
        k = k or rag_config.search_top_k

        if not self._qdrant_available:
            # Return empty results when Qdrant is not available
            logger.warning("Qdrant not available, returning empty search results")
            return []

        # Combine query and selected text for search
        combined_query = f"{query} Context: {selected_text}"

        # Generate embedding for the combined query
        if EMBEDDING_AVAILABLE and self.embedding_model:
            query_embedding = self.embedding_model.encode(combined_query).tolist()
        else:
            # Fallback: use a simple embedding (all zeros with correct dimension)
            # This will return documents but without semantic similarity
            query_embedding = [0.0] * self._embedding_size
            logger.warning("Using zero embedding for query as embedding model is not available. Search will return random results.")

        # Perform search in Qdrant
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=k
            )
        except AttributeError as e:
            logger.error(f"Qdrant client attribute error in search_with_selected_text: {e}")
            return []
        except Exception as e:
            logger.error(f"Qdrant search failed in search_with_selected_text: {e}")
            return []

        # Format results
        formatted_results = []
        for result in results:
            doc_info = {
                'id': result.id,
                'metadata': result.payload,
                'content': result.payload.get('content', '')
            }
            formatted_results.append((doc_info, float(result.score)))

        return formatted_results

    def delete_collection(self):
        """Delete the entire collection (use with caution!)"""
        if not self._qdrant_available:
            logger.warning("Qdrant not available, skipping collection deletion")
            return
        self.client.delete_collection(self.collection_name)
        logger.info(f"Deleted collection '{self.collection_name}'")

    def get_document_count(self) -> int:
        """Get the number of documents in the collection"""
        if not self._qdrant_available:
            logger.warning("Qdrant not available, returning 0 document count")
            return 0
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the collection (use with caution for large collections)"""
        if not self._qdrant_available:
            logger.warning("Qdrant not available, returning empty document list")
            return []

        # Scroll through all points in the collection
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000  # Adjust as needed
        )

        documents = []
        for point in points:
            doc_info = {
                'id': point.id,
                'metadata': point.payload,
                'content': point.payload.get('content', '')
            }
            documents.append(doc_info)

        return documents


def create_qdrant_store(collection_name: str = None) -> QdrantTextbookStore:
    """Create and return a Qdrant textbook store instance"""
    return QdrantTextbookStore(collection_name=collection_name)


if __name__ == "__main__":
    # Example usage
    print("Creating Qdrant store...")

    # Create store instance
    store = QdrantTextbookStore()

    # Sample documents
    sample_docs = [
        {
            'id': 'doc1',
            'content': 'Physical AI combines robotics and artificial intelligence to create embodied systems.',
            'metadata': {'title': 'Introduction to Physical AI', 'chapter': 'Chapter 1', 'relative_path': '/docs/chapter-1/intro'}
        },
        {
            'id': 'doc2',
            'content': 'Humanoid robots have multiple degrees of freedom and mimic human movement patterns.',
            'metadata': {'title': 'Humanoid Systems', 'chapter': 'Chapter 3', 'relative_path': '/docs/chapter-3/humanoid'}
        }
    ]

    # Add documents
    store.add_documents(sample_docs)

    # Test search
    results = store.search("What is Physical AI?", k=2)
    print(f"Search results: {results}")

    print(f"Total documents in collection: {store.get_document_count()}")