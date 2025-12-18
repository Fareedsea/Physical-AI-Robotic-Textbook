# Physical AI & Humanoid Robotics Textbook RAG System - Setup Guide

## Overview
This document provides setup instructions for the RAG (Retrieval-Augmented Generation) chatbot system for the Physical AI & Humanoid Robotics Textbook. The system uses OpenAI API, Qdrant Cloud for vector storage, and FastAPI for the backend API.

## System Architecture
- **Backend**: FastAPI server with OpenAI integration
- **Vector Database**: Qdrant Cloud (with fallback mode)
- **Frontend**: React chatbot component integrated with Docusaurus
- **Database**: Neon Postgres for conversation history and metadata

## Prerequisites
- Python 3.9+
- Node.js (for Docusaurus frontend)
- OpenAI API key
- Qdrant Cloud account (optional - system works in fallback mode without it)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Physical-AI-Robotic-Textbook
```

### 2. Set up Backend Environment

#### Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

**Note**: If you encounter Windows path length issues with torch/sentence-transformers installation, you may need to:
- Enable Windows long path support, or
- Use the system in fallback mode (without semantic search capabilities)

#### Create environment file:
```bash
cp .env.example .env
```

#### Configure environment variables:
Edit the `.env` file with your actual credentials:

```env
# Qdrant Configuration (get from Qdrant Cloud dashboard)
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=textbook_content

# OpenAI Configuration (get from OpenAI dashboard)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4 if preferred

# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Search Configuration
SEARCH_TOP_K=5
MIN_RELEVANCE_SCORE=0.3

# Chat Configuration
MAX_TOKENS=500
TEMPERATURE=0.7

# Hallucination Prevention Configuration
HALLUCINATION_PREVENTION_ENABLED=true
HALLUCINATION_THRESHOLD=0.15

# Textbook-specific settings
TEXTBOOK_DOCS_PATH=my-website/docs
```

### 3. Set up Frontend (Docusaurus)

```bash
cd ../my-website
npm install
```

### 4. Start the Services

#### Start the backend API server:
```bash
cd ../backend
uvicorn main:app --reload
```

#### In a new terminal, start the Docusaurus frontend:
```bash
cd ../my-website
npm run start
```

## Configuration Options

### With Qdrant Cloud (Full Functionality)
1. Sign up for Qdrant Cloud at [qdrant.tech](https://qdrant.tech/)
2. Create a collection and get your URL and API key
3. Add credentials to your `.env` file
4. Index your documents using:
```bash
python -m backend.scripts.index_documents
```

### Without Qdrant Cloud (Fallback Mode)
The system will work in fallback mode without Qdrant:
- Semantic search will not function
- The system will still connect to OpenAI for responses
- Text grounding features will be limited
- Qdrant operations will return empty results gracefully

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Chat Functionality
- `POST /chat/query` - Query the textbook chatbot
- `GET /chat/history` - Get conversation history
- `POST /chat/feedback` - Submit feedback for a response

### Content Search
- `GET /content/search` - Search textbook content
- `POST /content/search` - Search textbook content (with filters)

### API Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Frontend Integration

The chatbot is integrated into the Docusaurus site at the top right of each page. Users can:
- Ask questions about the textbook content
- Select text to ground their questions in specific content
- View sources for the chatbot's responses
- Rate responses and provide feedback

## Troubleshooting

### Common Issues:

1. **Long Path Issues on Windows**:
   - If installation fails due to long paths, enable Windows long path support or use fallback mode

2. **OpenAI API Key Issues**:
   - Ensure your OpenAI API key is correctly set in the `.env` file
   - Check that your OpenAI account has sufficient credits

3. **Qdrant Connection Issues**:
   - Verify your Qdrant Cloud URL and API key are correct
   - The system will work in fallback mode if Qdrant is unavailable

4. **Dependency Installation Issues**:
   - Try installing packages individually if the requirements.txt installation fails
   - Consider using a virtual environment

### Development Mode:
For development, you can run the system with partial functionality:
- Without Qdrant: Semantic search won't work, but OpenAI integration will
- Without OpenAI key: The system will return error messages but API will be accessible
- With both: Full functionality including semantic search and AI responses

## Testing

### Run validation:
```bash
python backend/simple_validation.py
```

### Run tests:
```bash
python backend/test_chatbot.py
```

## Deployment

### Backend Deployment:
The FastAPI application can be deployed to any Python-compatible hosting service (Heroku, AWS, GCP, etc.)

### Frontend Deployment:
The Docusaurus site can be deployed using standard static hosting services

## Security Considerations

- Never commit API keys or sensitive credentials
- Use environment variables for all secrets
- Implement rate limiting in production
- Validate and sanitize all user inputs
- Use HTTPS in production deployments

## Performance Notes

- The system uses fallback mechanisms when external services are unavailable
- Response times depend on OpenAI API performance
- Semantic search requires proper Qdrant configuration
- Consider caching for frequently asked questions in production