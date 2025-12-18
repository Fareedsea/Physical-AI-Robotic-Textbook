#!/usr/bin/env python3
"""
Simple validation script for the Physical AI & Humanoid Robotics Textbook RAG system
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

def validate_imports():
    """Validate that all required modules can be imported"""
    print("Validating imports...")

    try:
        from rag.new_config import rag_config
        print("[OK] Config module imported successfully")
        print(f"   OpenAI Model: {rag_config.openai_model}")
        print(f"   Qdrant Collection: {rag_config.qdrant_collection_name}")
    except Exception as e:
        print(f"[ERROR] Config import failed: {e}")
        return False

    try:
        from rag.qdrant_store import QdrantTextbookStore
        print("[OK] Qdrant store module imported successfully")
    except Exception as e:
        print(f"[ERROR] Qdrant store import failed: {e}")
        return False

    try:
        from rag.openai_chatbot import OpenAITextbookChatbot
        print("[OK] OpenAI chatbot module imported successfully")
    except Exception as e:
        print(f"[ERROR] OpenAI chatbot import failed: {e}")
        return False

    try:
        from rag.indexer import TextbookIndexer
        print("[OK] Indexer module imported successfully")
    except Exception as e:
        print(f"[ERROR] Indexer import failed: {e}")
        return False

    try:
        from rag.document_loader import load_textbook_documents
        print("[OK] Document loader module imported successfully")
    except Exception as e:
        print(f"[ERROR] Document loader import failed: {e}")
        return False

    return True

def validate_document_loading():
    """Validate that we can load textbook documents"""
    print("\nValidating document loading...")

    try:
        from rag.document_loader import load_textbook_documents
        from rag.new_config import rag_config

        docs_path = rag_config.textbook_docs_path
        print(f"   Looking for documents in: {docs_path}")

        if os.path.exists(docs_path):
            documents = load_textbook_documents(docs_path=docs_path)
            print(f"[OK] Successfully loaded {len(documents)} documents")
            if documents:
                print(f"   First document title: {documents[0]['metadata'].get('title', 'Unknown')}")
                print(f"   First document path: {documents[0]['metadata'].get('relative_path', 'Unknown')}")
        else:
            print(f"[WARN] Documents path does not exist: {docs_path}")
            print("   This is expected if the textbook content hasn't been created yet")

        return True
    except Exception as e:
        print(f"[ERROR] Document loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_api_endpoints():
    """Validate that API endpoints can be imported"""
    print("\nValidating API endpoints...")

    try:
        from api.endpoints import chat, content
        print("[OK] API endpoints imported successfully")
        print(f"   Chat router: {chat.router}")
        print(f"   Content router: {content.router}")
        return True
    except Exception as e:
        print(f"[ERROR] API endpoints import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main validation function"""
    print("Starting RAG System Validation")
    print("=" * 50)

    # Validate imports
    imports_ok = validate_imports()

    # Validate document loading
    docs_ok = validate_document_loading()

    # Validate API endpoints
    api_ok = validate_api_endpoints()

    print("\n" + "=" * 50)
    print("Validation Summary:")
    print(f"  Module imports: {'[OK] PASS' if imports_ok else '[ERROR] FAIL'}")
    print(f"  Document loading: {'[OK] PASS' if docs_ok else '[ERROR] FAIL (may be OK if no documents exist yet)'}")
    print(f"  API endpoints: {'[OK] PASS' if api_ok else '[ERROR] FAIL'}")

    overall_success = imports_ok and api_ok  # Don't require docs for basic validation
    print(f"  Overall: {'[OK] VALIDATION PASSED' if overall_success else '[ERROR] VALIDATION FAILED'}")

    return overall_success

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] RAG system validation completed successfully!")
        print("\nNext steps:")
        print("1. Set up your OpenAI API key in environment variables")
        print("2. Index your textbook documents using: python -m backend.scripts.index_documents")
        print("3. Start the API server: uvicorn backend.main:app --reload")
        print("4. Test the chatbot functionality")
    else:
        print("\n[ERROR] Validation failed. Please check the error messages above.")

    sys.exit(0 if success else 1)