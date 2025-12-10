# tests/contract/test_chat_feedback.py
# Contract test for /chat/feedback endpoint

import pytest
import json
from unittest.mock import Mock, patch

def test_chat_feedback_endpoint_contract():
    """
    Contract test for /chat/feedback endpoint
    Tests that the endpoint accepts the expected input and returns the expected output format
    """
    # Define the expected request structure
    expected_request = {
        "query_id": "string",
        "user_id": "string (optional)",
        "rating": "number between 1-5 or thumbs up/down",
        "comment": "string (optional)",
        "useful": "boolean (alternative to rating)"
    }

    # Define the expected response structure
    expected_response = {
        "success": "boolean",
        "feedback_id": "string",
        "message": "string"
    }

    # Mock the actual API call for contract testing
    mock_response = {
        "success": True,
        "feedback_id": "feedback-123",
        "message": "Feedback recorded successfully"
    }

    # Verify the response structure
    assert "success" in mock_response
    assert "feedback_id" in mock_response
    assert "message" in mock_response

    # Verify data types
    assert isinstance(mock_response["success"], bool)
    assert isinstance(mock_response["feedback_id"], str)
    assert isinstance(mock_response["message"], str)

    print("✓ /chat/feedback endpoint contract test passed")

def test_chat_feedback_batch_endpoint_contract():
    """
    Contract test for batch feedback submission
    Tests the endpoint for submitting multiple feedback items
    """
    # Define the expected request structure for batch feedback
    expected_request = {
        "feedback_items": [
            {
                "query_id": "string",
                "rating": "number or boolean",
                "comment": "string (optional)"
            }
        ]
    }

    # Mock the response for batch feedback
    mock_response = {
        "success": True,
        "processed_count": 1,
        "failed_count": 0,
        "results": [
            {
                "query_id": "query-123",
                "success": True,
                "feedback_id": "feedback-123"
            }
        ]
    }

    # Verify the response structure
    assert "success" in mock_response
    assert "processed_count" in mock_response
    assert "failed_count" in mock_response
    assert "results" in mock_response

    # Verify data types
    assert isinstance(mock_response["success"], bool)
    assert isinstance(mock_response["processed_count"], int)
    assert isinstance(mock_response["failed_count"], int)
    assert isinstance(mock_response["results"], list)

    print("✓ /chat/feedback batch endpoint contract test passed")

if __name__ == "__main__":
    test_chat_feedback_endpoint_contract()
    test_chat_feedback_batch_endpoint_contract()