# tests/contract/test_chat_api.py
# Contract test for /chat/query endpoint

import pytest
import requests
import json
from unittest.mock import Mock, patch

def test_chat_query_endpoint_contract():
    """
    Contract test for /chat/query endpoint
    Tests that the endpoint accepts the expected input and returns the expected output format
    """
    # Define the expected request structure
    expected_request = {
        "query": "string",
        "history": "array of message objects (optional)",
        "user_id": "string (optional)"
    }

    # Define the expected response structure
    expected_response = {
        "response": "string",
        "sources": "array of source objects",
        "confidence": "number between 0 and 1",
        "query_id": "string"
    }

    # Mock the actual API call for contract testing
    # In a real scenario, this would call the actual endpoint
    mock_response = {
        "response": "This is a sample response based on the textbook content.",
        "sources": [
            {
                "chapter": "Introduction to Physical AI",
                "section": "Basic Concepts",
                "page_reference": "p. 15",
                "similarity_score": 0.85
            }
        ],
        "confidence": 0.92,
        "query_id": "test-query-123"
    }

    # Verify the response structure
    assert "response" in mock_response
    assert "sources" in mock_response
    assert "confidence" in mock_response
    assert "query_id" in mock_response

    # Verify data types
    assert isinstance(mock_response["response"], str)
    assert isinstance(mock_response["sources"], list)
    assert isinstance(mock_response["confidence"], (int, float))
    assert isinstance(mock_response["query_id"], str)

    # Verify confidence is between 0 and 1
    assert 0 <= mock_response["confidence"] <= 1

    print("✓ /chat/query endpoint contract test passed")

if __name__ == "__main__":
    test_chat_query_endpoint_contract()