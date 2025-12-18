#!/usr/bin/env python3
"""
Script to index textbook documents into Qdrant vector store
"""

import sys
import os
import argparse
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.document_loader import load_textbook_documents
from rag.qdrant_store import QdrantTextbookStore
from rag.new_config import rag_config


def index_documents(docs_path: str = None, collection_name: str = None):
    """
    Index textbook documents into Qdrant

    Args:
        docs_path: Path to textbook documents (defaults to config value)
        collection_name: Qdrant collection name (defaults to config value)
    """
    docs_path = docs_path or rag_config.textbook_docs_path
    collection_name = collection_name or rag_config.qdrant_collection_name

    print(f"Loading documents from: {docs_path}")

    # Load documents
    documents = load_textbook_documents(docs_path=docs_path)
    print(f"Loaded {len(documents)} documents")

    if not documents:
        print("No documents found to index. Please check the docs path.")
        return

    # Initialize Qdrant store
    print(f"Initializing Qdrant store with collection: {collection_name}")
    qdrant_store = QdrantTextbookStore(collection_name=collection_name)

    # Add documents to Qdrant
    print("Adding documents to Qdrant...")
    qdrant_store.add_documents(documents)

    # Print summary
    doc_count = qdrant_store.get_document_count()
    print(f"Successfully indexed {doc_count} documents into Qdrant collection '{collection_name}'")


def main():
    parser = argparse.ArgumentParser(description="Index textbook documents into Qdrant")
    parser.add_argument(
        "--docs-path",
        type=str,
        default=None,
        help="Path to textbook documents (default: from config)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default=None,
        help="Qdrant collection name (default: from config)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be indexed without actually indexing"
    )

    args = parser.parse_args()

    if args.dry_run:
        docs_path = args.docs_path or rag_config.textbook_docs_path
        print(f"DRY RUN: Would load documents from: {docs_path}")

        documents = load_textbook_documents(docs_path=docs_path)
        print(f"Would index {len(documents)} documents")

        for i, doc in enumerate(documents[:5]):  # Show first 5 documents
            print(f"  {i+1}. {doc['metadata'].get('title', 'Untitled')} "
                  f"({len(doc['content'])} chars)")

        if len(documents) > 5:
            print(f"  ... and {len(documents) - 5} more documents")
    else:
        index_documents(docs_path=args.docs_path, collection_name=args.collection_name)


if __name__ == "__main__":
    main()