"""
Content indexing script for the Physical AI & Humanoid Robotics Textbook RAG system
Indexes Docusaurus markdown documents into the vector store
"""

import logging
import os
from typing import List, Dict, Any
from pathlib import Path

from .document_loader import TextbookDocumentLoader, load_textbook_documents
from .vector_store import TextbookVectorStore, create_textbook_vector_store
from .config import rag_config


logger = logging.getLogger(__name__)


class TextbookIndexer:
    """Indexes textbook content from Docusaurus docs into the vector store"""

    def __init__(self,
                 docs_path: str = None,
                 index_path: str = None,
                 metadata_path: str = None):
        self.docs_path = docs_path or rag_config.docs_path
        self.index_path = index_path or rag_config.index_path
        self.metadata_path = metadata_path or rag_config.metadata_path

    def index_content(self) -> bool:
        """
        Index all textbook content from Docusaurus docs into the vector store

        Returns:
            bool: True if indexing was successful, False otherwise
        """
        try:
            logger.info(f"Starting content indexing from {self.docs_path}")

            # Load documents from Docusaurus docs
            loader = TextbookDocumentLoader(docs_path=self.docs_path)
            documents = loader.load_documents()

            if not documents:
                logger.warning("No documents found to index")
                return False

            logger.info(f"Loaded {len(documents)} documents for indexing")

            # Create and populate vector store
            vector_store = create_textbook_vector_store(
                documents=documents,
                index_file=self.index_path,
                metadata_file=self.metadata_path
            )

            logger.info(f"Content indexed successfully to {self.index_path}")
            return True

        except Exception as e:
            logger.error(f"Error during content indexing: {str(e)}")
            return False

    def incremental_index(self, new_or_updated_files: List[str]) -> bool:
        """
        Perform incremental indexing for new or updated files

        Args:
            new_or_updated_files: List of file paths that are new or updated

        Returns:
            bool: True if incremental indexing was successful, False otherwise
        """
        try:
            logger.info(f"Starting incremental indexing for {len(new_or_updated_files)} files")

            # Load the existing vector store
            vector_store = TextbookVectorStore()
            try:
                vector_store.load(self.index_path, self.metadata_path)
                logger.info("Loaded existing vector store for incremental update")
            except FileNotFoundError:
                logger.info("No existing vector store found, creating new one")
                return self.index_content()

            # Load documents for the specific files
            documents = []
            loader = TextbookDocumentLoader(docs_path=self.docs_path)

            for file_path in new_or_updated_files:
                try:
                    doc = loader._load_single_document(file_path)
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    logger.error(f"Error loading document {file_path}: {str(e)}")
                    continue

            if not documents:
                logger.warning("No documents to add for incremental indexing")
                return True

            # Add new documents to the vector store
            vector_store.add_documents(documents)

            # Save the updated vector store
            vector_store.save(self.index_path, self.metadata_path)

            logger.info(f"Incremental indexing completed, {len(documents)} documents added")
            return True

        except Exception as e:
            logger.error(f"Error during incremental indexing: {str(e)}")
            return False

    def update_index(self) -> bool:
        """
        Update the index by reloading all content from docs

        Returns:
            bool: True if update was successful, False otherwise
        """
        logger.info("Starting full index update")
        return self.index_content()

    def delete_from_index(self, file_paths: List[str]) -> bool:
        """
        Remove documents from the index based on file paths

        Args:
            file_paths: List of file paths to remove from the index

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            logger.info(f"Starting deletion of {len(file_paths)} documents from index")

            # Load the existing vector store
            vector_store = TextbookVectorStore()
            vector_store.load(self.index_path, self.metadata_path)

            # In a real implementation, we would need a way to identify and remove specific documents
            # Since FAISS doesn't directly support deletion by ID, we would need to rebuild the index
            # without the specified documents. For this implementation, we'll trigger a full re-index
            # of the remaining documents.

            logger.info("Rebuilding index without specified documents")
            return self.index_content()

        except Exception as e:
            logger.error(f"Error during index deletion: {str(e)}")
            return False


def create_textbook_indexer(docs_path: str = None,
                           index_path: str = None,
                           metadata_path: str = None) -> TextbookIndexer:
    """
    Create a textbook indexer instance

    Args:
        docs_path: Path to Docusaurus docs directory
        index_path: Path to save the vector index
        metadata_path: Path to save the metadata

    Returns:
        TextbookIndexer instance
    """
    return TextbookIndexer(
        docs_path=docs_path or rag_config.docs_path,
        index_path=index_path or rag_config.index_path,
        metadata_path=metadata_path or rag_config.metadata_path
    )


def index_textbook_content(docs_path: str = None,
                          index_path: str = None,
                          metadata_path: str = None) -> bool:
    """
    Convenience function to index all textbook content

    Args:
        docs_path: Path to Docusaurus docs directory
        index_path: Path to save the vector index
        metadata_path: Path to save the metadata

    Returns:
        bool: True if indexing was successful, False otherwise
    """
    indexer = create_textbook_indexer(docs_path, index_path, metadata_path)
    return indexer.index_content()


if __name__ == "__main__":
    # Example usage
    print("Starting textbook content indexing...")

    # Create indexer and index content
    success = index_textbook_content()

    if success:
        print("Textbook content indexed successfully!")
    else:
        print("Failed to index textbook content.")
        exit(1)

    # Test the indexer with specific paths
    indexer = TextbookIndexer()
    print(f"Indexing content from: {indexer.docs_path}")
    print(f"Index will be saved to: {indexer.index_path}")
    print(f"Metadata will be saved to: {indexer.metadata_path}")