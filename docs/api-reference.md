# API Reference

## Overview

The Physical AI & Humanoid Robotics Textbook provides a RESTful API for interacting with the RAG (Retrieval-Augmented Generation) system. All API endpoints follow REST principles and return JSON responses.

## Base URL

All API requests are made to:
```
http://localhost:8000/api/  # Development
https://your-deployment.com/api/  # Production
```

## Authentication

The API does not require authentication for basic functionality, but user identification is supported through optional `user_id` parameters.

## Error Handling

All API endpoints return standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Resource Not Found
- `500`: Internal Server Error

Error responses include a descriptive message:

```json
{
  "detail": "Error description"
}
```

## Endpoints

### Chat API

#### POST /api/chat/query

Query the textbook chatbot with a question.

**Request Body:**
```json
{
  "query": "What is Physical AI?",
  "user_id": "optional_user_id",
  "session_id": "optional_session_id",
  "history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Parameters:**
- `query` (string, required): The user's question (1-2000 characters)
- `user_id` (string, optional): User identifier for tracking
- `session_id` (string, optional): Session identifier
- `history` (array, optional): Conversation history

**Response:**
```json
{
  "response": "Physical AI combines robotics and artificial intelligence...",
  "sources": [
    {
      "id": "doc123",
      "title": "Introduction to Physical AI",
      "chapter": "Chapter 1",
      "section": "introduction",
      "content_snippet": "Physical AI combines robotics and artificial intelligence...",
      "similarity_score": 0.85,
      "source_url": "/docs/chapter-1-basics-physical-ai/intro"
    }
  ],
  "confidence": 0.85,
  "query_id": "query_123456",
  "user_id": "user_123",
  "timestamp": "2023-10-01T12:00:00Z"
}
```

**Response Fields:**
- `response` (string): The chatbot's response
- `sources` (array): List of sources used to generate the response
- `confidence` (number): Confidence score (0.0-1.0)
- `query_id` (string): Unique identifier for the query
- `user_id` (string): User identifier
- `timestamp` (string): ISO 8601 timestamp

#### GET /api/chat/history

Get conversation history for a user.

**Query Parameters:**
- `user_id` (string, required): User identifier
- `session_id` (string, optional): Session identifier
- `limit` (integer, optional): Number of history items to return (default: 10, max: 100)
- `offset` (integer, optional): Offset for pagination (default: 0)

**Response:**
```json
{
  "history": [
    {
      "query": "What is Physical AI?",
      "response": "Physical AI combines robotics and artificial intelligence...",
      "sources": [...],
      "timestamp": "2023-10-01T12:00:00Z"
    }
  ],
  "total_count": 1,
  "has_more": false
}
```

#### POST /api/chat/feedback

Submit feedback for a chat response.

**Request Body:**
```json
{
  "query_id": "query_123456",
  "user_id": "optional_user_id",
  "rating": 5,
  "useful": true,
  "comment": "Great answer, very helpful"
}
```

**Parameters:**
- `query_id` (string, required): ID of the query being rated
- `user_id` (string, optional): User identifier
- `rating` (integer, optional): Rating from 1-5
- `useful` (boolean, optional): Whether the response was useful
- `comment` (string, optional): Additional feedback comment (max 1000 chars)

**Response:**
```json
{
  "success": true,
  "feedback_id": "feedback_abc123",
  "message": "Feedback recorded successfully"
}
```

### Content API

#### POST /api/content/search

Search textbook content using vector similarity.

**Request Body:**
```json
{
  "query": "control systems in robotics",
  "filters": {
    "chapter": "Chapter 5"
  },
  "max_results": 10,
  "min_relevance": 0.3
}
```

**Parameters:**
- `query` (string, required): Search query (1-1000 characters)
- `filters` (object, optional): Additional filters for search
- `max_results` (integer, optional): Maximum results to return (1-50, default: 10)
- `min_relevance` (number, optional): Minimum relevance threshold (0.0-1.0, default: 0.0)

**Response:**
```json
{
  "results": [
    {
      "id": "doc123",
      "title": "Control Systems in Robotics",
      "content_snippet": "Control systems are fundamental to robotics...",
      "chapter": "Chapter 5",
      "section": "control-systems",
      "similarity_score": 0.85,
      "source_url": "/docs/chapter-5-control-systems/core-concepts"
    }
  ],
  "total_count": 1,
  "query_id": "search_456789",
  "execution_time": 23.4
}
```

**Response Fields:**
- `results` (array): List of search results
- `total_count` (integer): Total number of results found
- `query_id` (string): Unique identifier for this query
- `execution_time` (number): Time taken to execute the search in milliseconds

#### GET /api/content/search

Simple search endpoint using query parameters.

**Query Parameters:**
- `query` (string, required): Search query (1-1000 characters)
- `max_results` (integer, optional): Maximum results to return (1-50, default: 10)
- `min_relevance` (number, optional): Minimum relevance threshold (0.0-1.0, default: 0.0)

**Response:**
Same as POST /api/content/search

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per IP address

Rate limit exceeded responses include the following headers:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time when the limit resets

## Examples

### JavaScript (using fetch)

```javascript
// Query the chatbot
fetch('/api/chat/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'What is Physical AI?',
    user_id: 'user_123'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Search content
fetch('/api/content/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'control systems',
    max_results: 5
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python (using requests)

```python
import requests

# Query the chatbot
response = requests.post('/api/chat/query', json={
    'query': 'What is Physical AI?',
    'user_id': 'user_123'
})
data = response.json()
print(data['response'])

# Search content
response = requests.post('/api/content/search', json={
    'query': 'control systems',
    'max_results': 5
})
data = response.json()
for result in data['results']:
    print(f"{result['title']}: {result['content_snippet'][:100]}...")
```

## SDKs and Libraries

### JavaScript Client

A JavaScript client library is available for easy integration:

```bash
npm install @physical-ai/textbook-client
```

```javascript
import { TextbookClient } from '@physical-ai/textbook-client';

const client = new TextbookClient({ baseURL: 'https://your-api.com' });

// Query chatbot
const response = await client.chat.query('What is Physical AI?');
console.log(response.response);

// Search content
const results = await client.content.search('control systems');
console.log(results);
```

## Testing the API

You can test the API endpoints using tools like:
- Postman
- curl
- FastAPI's built-in Swagger UI at `/docs`
- Python requests library

## Versioning

The API follows semantic versioning. Breaking changes will increment the major version number. Current version: v1.