#!/usr/bin/env python3
"""
Test script for the Physical AI & Humanoid Robotics Textbook RAG chatbot
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from rag.openai_chatbot import OpenAITextbookChatbot, create_openai_chatbot
from rag.qdrant_store import QdrantTextbookStore
from rag.new_config import rag_config


def test_chatbot_functionality():
    """Test the basic functionality of the chatbot"""
    print("Testing OpenAI Textbook Chatbot functionality...")

    try:
        # Create Qdrant store
        print("1. Creating Qdrant store...")
        qdrant_store = QdrantTextbookStore()
        print(f"   Qdrant store created with collection: {qdrant_store.collection_name}")

        # Create chatbot
        print("2. Creating OpenAI chatbot...")
        chatbot = create_openai_chatbot(qdrant_store=qdrant_store)
        print("   Chatbot created successfully")

        # Test basic query
        print("3. Testing basic query...")
        test_query = "What is Physical AI?"
        response = chatbot.get_response(
            query=test_query,
            user_id="test_user",
            session_id="test_session"
        )

        print(f"   Query: {test_query}")
        print(f"   Response: {response['response'][:200]}...")
        print(f"   Confidence: {response['confidence']:.3f}")
        print(f"   Sources: {len(response['sources'])} documents")

        # Test with selected text context
        print("4. Testing with selected text context...")
        selected_text = "Physical AI combines robotics and artificial intelligence to create embodied systems."
        response_with_context = chatbot.get_response(
            query="Explain this concept further",
            user_id="test_user",
            session_id="test_session",
            selected_text=selected_text
        )

        print(f"   Selected text: {selected_text}")
        print(f"   Query: Explain this concept further")
        print(f"   Response: {response_with_context['response'][:200]}...")

        # Test hallucination prevention
        print("5. Testing hallucination prevention...")
        # This test will depend on whether there's relevant context in the vector store
        # If there's no context, the response should be flagged for potential hallucination
        no_context_query = "What is the secret to eternal life according to the textbook?"
        response_no_context = chatbot.get_response(
            query=no_context_query,
            user_id="test_user",
            session_id="test_session"
        )

        print(f"   Query: {no_context_query}")
        print(f"   Response: {response_no_context['response'][:200]}...")
        print(f"   Confidence: {response_no_context['confidence']:.3f}")

        print("\n✅ All tests completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_indexing_functionality():
    """Test the document indexing functionality"""
    print("\nTesting document indexing functionality...")

    try:
        from rag.indexer import TextbookIndexer

        # Create indexer
        print("1. Creating textbook indexer...")
        indexer = TextbookIndexer(docs_path=rag_config.textbook_docs_path)
        print(f"   Indexer created for path: {indexer.docs_path}")

        # Get initial stats
        print("2. Getting initial index stats...")
        initial_stats = indexer.get_index_stats()
        print(f"   Initial stats: {initial_stats}")

        # Index documents
        print("3. Indexing documents...")
        result = indexer.index_documents()
        print(f"   Indexing result: {result}")

        # Get final stats
        print("4. Getting final index stats...")
        final_stats = indexer.get_index_stats()
        print(f"   Final stats: {final_stats}")

        print("\n✅ Indexing tests completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during indexing testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("Starting RAG Chatbot Tests")
    print("=" * 50)

    # Test chatbot functionality
    chatbot_success = test_chatbot_functionality()

    # Test indexing functionality
    indexing_success = test_indexing_functionality()

    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"  Chatbot functionality: {'✅ PASS' if chatbot_success else '❌ FAIL'}")
    print(f"  Indexing functionality: {'✅ PASS' if indexing_success else '❌ FAIL'}")

    overall_success = chatbot_success and indexing_success
    print(f"  Overall: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")

    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)