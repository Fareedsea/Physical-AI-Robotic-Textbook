"""
Document indexing module for the Physical AI & Humanoid Robotics Textbook RAG system
Handles indexing of textbook documents into Qdrant vector store
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

from rag.document_loader import load_textbook_documents
from rag.qdrant_store import QdrantTextbookStore
from rag.new_config import rag_config

logger = logging.getLogger(__name__)


class TextbookIndexer:
    """Handles indexing of textbook documents into vector store"""

    def __init__(self, qdrant_store: QdrantTextbookStore = None, docs_path: str = None):
        self.qdrant_store = qdrant_store or QdrantTextbookStore()
        self.docs_path = Path(docs_path or rag_config.textbook_docs_path)

    def index_documents(self, docs_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Index textbook documents into Qdrant

        Args:
            docs_path: Path to textbook documents (optional, defaults to instance path)

        Returns:
            Dictionary with indexing results
        """
        start_time = time.time()
        docs_path = Path(docs_path or self.docs_path)

        logger.info(f"Starting document indexing from: {docs_path}")

        try:
            # Load documents
            documents = load_textbook_documents(docs_path=str(docs_path))
            logger.info(f"Loaded {len(documents)} documents")

            if not documents:
                logger.warning("No documents found to index")
                return {
                    "indexed_count": 0,
                    "total_documents": 0,
                    "processing_time": time.time() - start_time,
                    "success": True,
                    "message": "No documents found to index"
                }

            # Add documents to Qdrant
            logger.info("Adding documents to Qdrant...")
            self.qdrant_store.add_documents(documents)

            # Get final count
            final_count = self.qdrant_store.get_document_count()

            processing_time = time.time() - start_time

            logger.info(f"Successfully indexed {len(documents)} documents in {processing_time:.2f}s")
            logger.info(f"Total documents in store: {final_count}")

            return {
                "indexed_count": len(documents),
                "total_documents": final_count,
                "processing_time": processing_time,
                "success": True,
                "message": f"Successfully indexed {len(documents)} documents"
            }

        except Exception as e:
            logger.error(f"Error during document indexing: {str(e)}")
            return {
                "indexed_count": 0,
                "total_documents": 0,
                "processing_time": time.time() - start_time,
                "success": False,
                "message": f"Error during indexing: {str(e)}"
            }

    def update_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Update a single document in the vector store"""
        try:
            # Delete the existing document
            self.qdrant_store.client.delete(
                collection_name=self.qdrant_store.collection_name,
                points_selector=[doc_id]
            )

            # Add the updated document
            updated_doc = {
                'id': doc_id,
                'content': content,
                'metadata': metadata
            }
            self.qdrant_store.add_documents([updated_doc])

            logger.info(f"Updated document {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {str(e)}")
            return False

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store"""
        try:
            self.qdrant_store.client.delete(
                collection_name=self.qdrant_store.collection_name,
                points_selector=[doc_id]
            )
            logger.info(f"Deleted document {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {str(e)}")
            return False

    def reindex_all(self, docs_path: Optional[str] = None) -> Dict[str, Any]:
        """Delete existing collection and reindex all documents"""
        start_time = time.time()
        docs_path = Path(docs_path or self.docs_path)

        logger.info("Starting full reindexing...")

        try:
            # Delete the existing collection
            self.qdrant_store.delete_collection()
            logger.info("Deleted existing collection")

            # Create a new store instance (collection will be recreated automatically)
            self.qdrant_store = QdrantTextbookStore()

            # Index documents
            result = self.index_documents(docs_path=str(docs_path))
            result["processing_time"] = time.time() - start_time

            logger.info("Full reindexing completed")
            return result

        except Exception as e:
            logger.error(f"Error during full reindexing: {str(e)}")
            return {
                "indexed_count": 0,
                "total_documents": 0,
                "processing_time": time.time() - start_time,
                "success": False,
                "message": f"Error during reindexing: {str(e)}"
            }

    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index"""
        try:
            count = self.qdrant_store.get_document_count()
            collection_info = self.qdrant_store.client.get_collection(
                self.qdrant_store.collection_name
            )

            return {
                "document_count": count,
                "vectors_count": collection_info.vectors_count,
                "indexed": True,
                "collection_name": self.qdrant_store.collection_name
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {str(e)}")
            return {
                "document_count": 0,
                "vectors_count": 0,
                "indexed": False,
                "collection_name": self.qdrant_store.collection_name,
                "error": str(e)
            }


def create_indexer(qdrant_store: QdrantTextbookStore = None, docs_path: str = None) -> TextbookIndexer:
    """Create a textbook indexer instance"""
    return TextbookIndexer(qdrant_store=qdrant_store, docs_path=docs_path)


if __name__ == "__main__":
    # Example usage
    print("Creating textbook indexer...")

    # Create indexer
    indexer = TextbookIndexer()

    # Get initial stats
    stats = indexer.get_index_stats()
    print(f"Initial index stats: {stats}")

    # Index documents
    result = indexer.index_documents()
    print(f"Indexing result: {result}")

    # Get final stats
    final_stats = indexer.get_index_stats()
    print(f"Final index stats: {final_stats}")
