# Physical AI & Humanoid Robotics Textbook - Documentation

Welcome to the comprehensive documentation for the Physical AI & Humanoid Robotics Textbook project. This documentation covers all aspects of the project including architecture, API references, deployment instructions, and development guidelines.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [API Reference](#api-reference)
3. [Development Setup](#development-setup)
4. [Deployment Guide](#deployment-guide)
5. [RAG System](#rag-system)
6. [Integration Modules](#integration-modules)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

## Architecture Overview

The Physical AI & Humanoid Robotics Textbook is built using a modern web stack with the following key components:

- **Frontend**: Docusaurus-based static site for textbook content
- **Backend**: FastAPI-based RAG system for intelligent Q&A
- **Vector Store**: FAISS-based similarity search for textbook content
- **Integration Modules**: ROS 2, Gazebo, NVIDIA Isaac, and VLA system interfaces

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │  Vector Store   │
│   (Docusaurus)  │◄──►│   (FastAPI)      │◄──►│   (FAISS)       │
│                 │    │                  │    │                 │
│  - Textbook     │    │  - RAG Chatbot   │    │  - Embeddings   │
│    Content      │    │  - Search API    │    │  - Similarity   │
│  - Chat UI      │    │  - Content API   │    │    Search       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Integration     │
                    │  Modules         │
                    │  - ROS 2         │
                    │  - Gazebo        │
                    │  - NVIDIA Isaac  │
                    │  - VLA Systems   │
                    └──────────────────┘
```

## API Reference

### Chat API

#### POST /api/chat/query
Query the textbook chatbot with a question.

**Request Body:**
```json
{
  "query": "What is Physical AI?",
  "user_id": "optional_user_id",
  "session_id": "optional_session_id",
  "history": []
}
```

**Response:**
```json
{
  "response": "Physical AI combines robotics and artificial intelligence...",
  "sources": [...],
  "confidence": 0.85,
  "query_id": "query_123456",
  "user_id": "user_123",
  "timestamp": "2023-10-01T12:00:00Z"
}
```

#### GET /api/chat/history
Get conversation history for a user.

#### POST /api/chat/feedback
Submit feedback for a chat response.

### Content API

#### POST /api/content/search
Search textbook content using vector similarity.

## Development Setup

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip
- git

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the website directory:
```bash
cd my-website
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Deployment Guide

### GitHub Pages Deployment

The textbook is deployed to GitHub Pages using GitHub Actions. The workflow is defined in `.github/workflows/deploy.yml`.

### Environment Variables

For production deployment, set the following environment variables:

- `EMBEDDING_MODEL`: Model name for embeddings (default: "sentence-transformers/all-MiniLM-L6-v2")
- `MAX_TOKENS`: Maximum tokens for responses (default: 500)
- `TEMPERATURE`: Temperature for response generation (default: 0.7)
- `DOCS_PATH`: Path to textbook documents (default: "my-website/docs")
- `INDEX_PATH`: Path to vector index (default: "backend/data/textbook_index.faiss")
- `METADATA_PATH`: Path to metadata file (default: "backend/data/textbook_metadata.pkl")

## RAG System

### Configuration

The RAG system is configured through `backend/rag/config.py`. Key configuration options include:

- **Embedding Model**: Configures the sentence transformer model for embeddings
- **Vector Store**: Configures FAISS index parameters
- **Search Parameters**: Configures similarity search behavior
- **Content Processing**: Configures document chunking and preprocessing

### Indexing Process

1. Documents are loaded from the Docusaurus docs directory
2. Content is chunked into smaller pieces for better retrieval
3. Embeddings are generated for each chunk
4. Vector index is created and saved for fast similarity search

### Search Algorithm

The system uses cosine similarity for vector search with optional hybrid search combining semantic and keyword-based approaches.

## Integration Modules

### ROS 2 Integration

The ROS 2 integration module provides interfaces for textbook examples using ROS 2. It includes:

- Node configuration and management
- Example launching capabilities
- Environment information utilities

### Gazebo Integration

The Gazebo integration module enables simulation examples from the textbook:

- World configuration and management
- Model spawning capabilities
- Simulation control utilities

### NVIDIA Isaac Integration

The Isaac integration provides access to NVIDIA's robotics simulation platform:

- Application configuration and execution
- Robot asset management
- Behavior simulation capabilities

### VLA (Vision-Language-Action) Integration

The VLA system integration demonstrates multimodal AI capabilities:

- Vision-language-action processing pipeline
- Training utilities for VLA models
- Example scenarios for textbook concepts

## Testing

### Unit Tests

Unit tests are located in the `tests/` directory and can be run with:

```bash
# Backend tests
cd backend
python -m pytest tests/unit/

# Frontend tests
cd my-website
npm test
```

### Performance Tests

Performance tests are located in `tests/performance/` and can be run to validate:

- RAG response times
- Page load performance
- Load handling capabilities

## Troubleshooting

### Common Issues

#### Embedding Model Loading Issues
If the embedding model fails to load, ensure you have internet connectivity and sufficient disk space in your Hugging Face cache directory.

#### Vector Store Not Found
If the vector store is not found, you may need to rebuild it by running the indexing process:
```bash
python -c "from backend.rag.indexer import index_textbook_content; index_textbook_content()"
```

#### API Rate Limits
If experiencing API rate limits, consider implementing caching or reducing the frequency of requests.

### Getting Help

For additional support, please check:
- The GitHub issues for known problems
- The project's Discord/Slack channel (if available)
- The maintainers' contact information in the README