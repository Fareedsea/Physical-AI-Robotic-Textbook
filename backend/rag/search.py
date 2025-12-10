"""
Similarity search functionality for the Physical AI & Humanoid Robotics Textbook RAG system
Implements semantic search using vector embeddings and various search strategies
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from .config import rag_config, search_config
from .vector_store import TextbookVectorStore
from .document_loader import load_textbook_documents
import numpy as np
import faiss
import time

# Optional imports that might not be available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None


logger = logging.getLogger(__name__)


class TextbookSearcher:
    """Main class for performing similarity searches on textbook content"""

    def __init__(self, vector_store: TextbookVectorStore = None):
        """
        Initialize the searcher with a vector store

        Args:
            vector_store: Pre-initialized vector store, if None will be created
        """
        self.vector_store = vector_store or TextbookVectorStore()

        # Load the embedding model
        self.embedding_model = SentenceTransformer(rag_config.embedding.model_name)

        # Load the vector store if not already loaded
        if not self.vector_store.is_loaded():
            try:
                self.vector_store.load()
                logger.info("Vector store loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load existing vector store: {str(e)}. Vector store will be initialized empty.")

    def search(self,
               query: str,
               k: int = None,
               min_relevance: float = None,
               filters: Optional[Dict[str, Any]] = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Perform similarity search on textbook content

        Args:
            query: The search query string
            k: Number of results to return (defaults to config value)
            min_relevance: Minimum relevance threshold (defaults to config value)
            filters: Optional filters to apply to search results

        Returns:
            List of tuples containing (document_info, similarity_score)
        """
        if k is None:
            k = search_config.max_results
        if min_relevance is None:
            min_relevance = search_config.min_relevance_score

        start_time = time.time()

        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.encode([query])

            # Perform search in the vector store
            results = self.vector_store.search(query, k=k)

            # Apply minimum relevance filter
            filtered_results = [
                (doc_info, score)
                for doc_info, score in results
                if score >= min_relevance
            ]

            # Apply additional filters if provided
            if filters:
                filtered_results = self._apply_filters(filtered_results, filters)

            # Sort by similarity score (descending)
            filtered_results.sort(key=lambda x: x[1], reverse=True)

            # Limit to k results after filtering
            filtered_results = filtered_results[:k]

            search_time = time.time() - start_time
            logger.debug(f"Search completed in {search_time:.3f}s, found {len(filtered_results)} results")

            return filtered_results

        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []

    def hybrid_search(self,
                      query: str,
                      k: int = None,
                      min_relevance: float = None,
                      filters: Optional[Dict[str, Any]] = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Perform hybrid search combining semantic and keyword-based search

        Args:
            query: The search query string
            k: Number of results to return (defaults to config value)
            min_relevance: Minimum relevance threshold (defaults to config value)
            filters: Optional filters to apply to search results

        Returns:
            List of tuples containing (document_info, combined_score)
        """
        if not search_config.use_hybrid_search:
            # If hybrid search is disabled, fall back to semantic search
            return self.search(query, k, min_relevance, filters)

        if k is None:
            k = search_config.max_results
        if min_relevance is None:
            min_relevance = search_config.min_relevance_score

        start_time = time.time()

        try:
            # Perform semantic search
            semantic_results = self.search(query, k=k*2, min_relevance=0.0, filters=filters)

            # Perform keyword search (simplified implementation)
            keyword_results = self._keyword_search(query, k=k*2)

            # Combine scores using weighted approach
            combined_results = self._combine_search_results(
                semantic_results,
                keyword_results,
                search_config.semantic_weight,
                search_config.keyword_weight
            )

            # Apply minimum relevance filter
            filtered_results = [
                (doc_info, score)
                for doc_info, score in combined_results
                if score >= min_relevance
            ]

            # Sort by combined score (descending)
            filtered_results.sort(key=lambda x: x[1], reverse=True)

            # Limit to k results after filtering
            filtered_results = filtered_results[:k]

            search_time = time.time() - start_time
            logger.debug(f"Hybrid search completed in {search_time:.3f}s, found {len(filtered_results)} results")

            return filtered_results

        except Exception as e:
            logger.error(f"Error performing hybrid search: {str(e)}")
            # Fall back to semantic search if hybrid search fails
            return self.search(query, k, min_relevance, filters)

    def _keyword_search(self, query: str, k: int) -> List[Tuple[Dict[str, Any], float]]:
        """
        Simple keyword-based search for hybrid search implementation

        Args:
            query: The search query string
            k: Number of results to return

        Returns:
            List of tuples containing (document_info, keyword_score)
        """
        # This is a simplified implementation
        # In a real implementation, you might use Elasticsearch, Whoosh, or other full-text search engines
        all_docs = self.vector_store.get_all_documents()
        keyword_results = []

        query_lower = query.lower()

        for doc_info in all_docs:
            content = doc_info['metadata'].get('content', '').lower()
            title = doc_info['metadata'].get('title', '').lower()

            # Calculate a simple keyword match score
            content_matches = content.count(query_lower)
            title_matches = title.count(query_lower)

            # Weight title matches higher than content matches
            keyword_score = (title_matches * 0.3) + (content_matches * 0.1)

            if keyword_score > 0:
                keyword_results.append((doc_info, min(keyword_score, 1.0)))

        # Sort by keyword score
        keyword_results.sort(key=lambda x: x[1], reverse=True)

        return keyword_results[:k]

    def _combine_search_results(self,
                                semantic_results: List[Tuple[Dict[str, Any], float]],
                                keyword_results: List[Tuple[Dict[str, Any], float]],
                                semantic_weight: float,
                                keyword_weight: float) -> List[Tuple[Dict[str, Any], float]]:
        """
        Combine semantic and keyword search results using weighted scoring

        Args:
            semantic_results: Results from semantic search
            keyword_results: Results from keyword search
            semantic_weight: Weight for semantic scores
            keyword_weight: Weight for keyword scores

        Returns:
            Combined results with normalized scores
        """
        # Create a mapping of doc_id to combined score
        combined_scores = {}

        # Add semantic scores
        for doc_info, score in semantic_results:
            doc_id = doc_info.get('id', doc_info['metadata'].get('source', 'unknown'))
            combined_scores[doc_id] = {
                'doc_info': doc_info,
                'semantic_score': score,
                'keyword_score': 0.0
            }

        # Add keyword scores
        for doc_info, score in keyword_results:
            doc_id = doc_info.get('id', doc_info['metadata'].get('source', 'unknown'))
            if doc_id in combined_scores:
                combined_scores[doc_id]['keyword_score'] = score
            else:
                combined_scores[doc_id] = {
                    'doc_info': doc_info,
                    'semantic_score': 0.0,
                    'keyword_score': score
                }

        # Calculate combined scores
        final_results = []
        for doc_id, data in combined_scores.items():
            combined_score = (
                (data['semantic_score'] * semantic_weight) +
                (data['keyword_score'] * keyword_weight)
            )
            # Normalize to 0-1 range
            combined_score = min(combined_score, 1.0)
            final_results.append((data['doc_info'], combined_score))

        return final_results

    def _apply_filters(self,
                       results: List[Tuple[Dict[str, Any], float]],
                       filters: Dict[str, Any]) -> List[Tuple[Dict[str, Any], float]]:
        """
        Apply filters to search results

        Args:
            results: List of search results
            filters: Dictionary of filters to apply

        Returns:
            Filtered list of results
        """
        filtered_results = []

        for doc_info, score in results:
            metadata = doc_info['metadata']
            include = True

            for filter_key, filter_value in filters.items():
                if filter_key in metadata:
                    if isinstance(filter_value, list):
                        if metadata[filter_key] not in filter_value:
                            include = False
                            break
                    else:
                        if metadata[filter_key] != filter_value:
                            include = False
                            break
                else:
                    # If filter key doesn't exist in metadata, exclude the result
                    include = False
                    break

            if include:
                filtered_results.append((doc_info, score))

        return filtered_results


def create_textbook_searcher(vector_store_path: str = None,
                            metadata_path: str = None) -> TextbookSearcher:
    """
    Create a textbook searcher instance with optional custom paths

    Args:
        vector_store_path: Path to vector store file
        metadata_path: Path to metadata file

    Returns:
        TextbookSearcher instance
    """
    vector_store = TextbookVectorStore()

    if vector_store_path and metadata_path:
        vector_store.load(vector_store_path, metadata_path)
    else:
        try:
            vector_store.load()
        except:
            logger.info("No existing vector store found, will work with empty store")

    return TextbookSearcher(vector_store=vector_store)


if __name__ == "__main__":
    # Example usage
    print("Creating textbook searcher...")

    # Create searcher instance
    searcher = create_textbook_searcher()

    # Example search
    query = "What is Physical AI?"
    results = searcher.search(query, k=5)

    print(f"Search results for query: '{query}'")
    for i, (doc_info, score) in enumerate(results, 1):
        metadata = doc_info['metadata']
        print(f"{i}. Score: {score:.3f}")
        print(f"   Title: {metadata.get('title', 'Unknown')}")
        print(f"   Chapter: {metadata.get('chapter', 'Unknown')}")
        print(f"   Content preview: {metadata.get('content', '')[:100]}...")
        print()