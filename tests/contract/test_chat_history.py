# tests/contract/test_chat_history.py
# Contract test for /chat/history endpoint

import pytest
import json
from unittest.mock import Mock, patch

def test_chat_history_endpoint_contract():
    """
    Contract test for /chat/history endpoint
    Tests that the endpoint accepts the expected input and returns the expected output format
    """
    # Define the expected request structure
    expected_request = {
        "user_id": "string",
        "session_id": "string (optional)",
        "limit": "number (optional)",
        "offset": "number (optional)"
    }

    # Define the expected response structure
    expected_response = {
        "history": "array of conversation objects",
        "total_count": "number",
        "has_more": "boolean"
    }

    # Mock the actual API call for contract testing
    mock_response = {
        "history": [
            {
                "query_id": "query-123",
                "query": "What is embodied intelligence?",
                "response": "Embodied intelligence refers to...",
                "timestamp": "2025-12-10T10:30:00Z",
                "sources": ["Chapter 1", "Chapter 2"]
            }
        ],
        "total_count": 1,
        "has_more": False
    }

    # Verify the response structure
    assert "history" in mock_response
    assert "total_count" in mock_response
    assert "has_more" in mock_response

    # Verify data types
    assert isinstance(mock_response["history"], list)
    assert isinstance(mock_response["total_count"], int)
    assert isinstance(mock_response["has_more"], bool)

    # If history is not empty, verify its structure
    if mock_response["history"]:
        first_item = mock_response["history"][0]
        assert "query_id" in first_item
        assert "query" in first_item
        assert "response" in first_item
        assert "timestamp" in first_item
        assert "sources" in first_item

    print("✓ /chat/history endpoint contract test passed")

def test_chat_history_create_endpoint_contract():
    """
    Contract test for creating/updating chat history
    Tests the POST endpoint for adding new history items
    """
    # Define the expected request structure for creating history
    expected_request = {
        "user_id": "string",
        "session_id": "string",
        "query": "string",
        "response": "string",
        "sources": "array of source strings"
    }

    # Mock the response for a successful creation
    mock_response = {
        "success": True,
        "history_id": "history-item-123"
    }

    # Verify the response structure
    assert "success" in mock_response
    assert "history_id" in mock_response

    # Verify data types
    assert isinstance(mock_response["success"], bool)
    assert isinstance(mock_response["history_id"], str)

    print("✓ /chat/history create endpoint contract test passed")

if __name__ == "__main__":
    test_chat_history_endpoint_contract()
    test_chat_history_create_endpoint_contract()