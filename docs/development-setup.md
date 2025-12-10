# Development Setup Guide

This guide will help you set up your development environment to work on the Physical AI & Humanoid Robotics Textbook project.

## Prerequisites

Before starting, ensure you have the following installed on your system:

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: Minimum 5GB available space
- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher
- **npm**: Version 8 or higher (usually comes with Node.js)
- **Git**: Version 2.0 or higher

### Optional Requirements (for full functionality)
- **CUDA**: For GPU acceleration (if using NVIDIA GPU)
- **Docker**: For containerized development (optional)

## Quick Setup

For a quick setup, follow these steps:

1. **Clone the repository**:
```bash
git clone https://github.com/your-org/physical-ai-textbook.git
cd physical-ai-textbook
```

2. **Set up the backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up the frontend**:
```bash
cd ../my-website
npm install
```

4. **Start both services** (in separate terminals):
```bash
# Terminal 1: Start the backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Start the frontend
cd my-website
npm start
```

## Detailed Setup Instructions

### Backend Setup (Python)

1. **Create a virtual environment**:
```bash
cd backend
python -m venv venv
```

2. **Activate the virtual environment**:
```bash
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install additional dependencies if needed**:
```bash
# For development dependencies
pip install -r requirements-dev.txt
```

5. **Set up environment variables** (optional):
Create a `.env` file in the `backend` directory:
```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_TOKENS=500
TEMPERATURE=0.7
DOCS_PATH=my-website/docs
INDEX_PATH=backend/data/textbook_index.faiss
METADATA_PATH=backend/data/textbook_metadata.pkl
HF_HOME=/path/to/huggingface/cache
```

### Frontend Setup (Docusaurus/React)

1. **Navigate to the website directory**:
```bash
cd my-website
```

2. **Install Node.js dependencies**:
```bash
npm install
```

3. **Start the development server**:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`.

### Running Both Services Simultaneously

For development, you'll typically want both the backend and frontend running. You can use a process manager or run them in separate terminals:

**Option 1: Separate Terminals**
- Terminal 1: Backend server
- Terminal 2: Frontend server

**Option 2: Using concurrently (if installed)**
```bash
# From the project root
npx concurrently "cd backend && python -m venv venv && source venv/bin/activate && python -m uvicorn main:app --reload --port 8000" "cd my-website && npm start"
```

## Environment Configuration

### Backend Environment Variables

The backend can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Model for generating embeddings |
| `MAX_TOKENS` | `500` | Maximum tokens for responses |
| `TEMPERATURE` | `0.7` | Temperature for response generation |
| `DOCS_PATH` | `my-website/docs` | Path to textbook documents |
| `INDEX_PATH` | `backend/data/textbook_index.faiss` | Path to vector index |
| `METADATA_PATH` | `backend/data/textbook_metadata.pkl` | Path to metadata file |
| `HF_HOME` | `~/.cache/huggingface` | Hugging Face cache directory |

### Frontend Environment Variables

The frontend uses Docusaurus configuration, which can be customized in `docusaurus.config.ts`.

## Development Workflow

### Backend Development

1. **Code Structure**:
```
backend/
├── api/                 # API endpoints
│   └── endpoints/
├── rag/                # RAG system components
│   ├── __init__.py
│   ├── chatbot.py      # Chatbot service
│   ├── vector_store.py # Vector store implementation
│   ├── document_loader.py # Document loading
│   ├── search.py       # Search functionality
│   └── config.py       # Configuration
├── models/             # Data models
│   └── session.py      # Session management
├── integration/        # Integration modules
│   ├── ros2_integration.py
│   ├── gazebo_integration.py
│   ├── isaac_integration.py
│   └── vla_integration.py
├── main.py            # FastAPI app entry point
└── requirements.txt   # Python dependencies
```

2. **Running Tests**:
```bash
cd backend
python -m pytest tests/
```

3. **Code Formatting**:
```bash
# Using black for Python formatting
black .
```

### Frontend Development

1. **Code Structure**:
```
my-website/
├── src/
│   ├── components/     # React components
│   │   └── Chatbot/   # Chatbot component
│   ├── pages/         # Docusaurus pages
│   ├── utils/         # Utility functions
│   │   └── api-client.js # API client
│   └── css/           # Custom styles
├── docs/              # Textbook content
├── docusaurus.config.ts # Docusaurus configuration
└── package.json       # Node.js dependencies
```

2. **Development Commands**:
```bash
# Start development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve

# Run tests
npm test

# Format code
npm run format
```

## Database and Vector Store Setup

### Initial Indexing

To create the initial vector store from textbook content:

```bash
cd backend
python -c "from rag.indexer import index_textbook_content; index_textbook_content()"
```

### Updating the Index

When textbook content changes, re-index with:

```bash
python -c "from rag.indexer import index_textbook_content; index_textbook_content()"
```

## Testing

### Backend Tests

Run backend tests using pytest:

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests

Run frontend tests:

```bash
cd my-website
npm test
```

### End-to-End Tests

For end-to-end testing, ensure both backend and frontend are running, then:

```bash
# Example using a testing framework like Playwright
npm run test:e2e
```

## Common Development Tasks

### Adding New Textbook Content

1. Create new markdown files in `my-website/docs/`
2. Update `my-website/sidebars.ts` to include the new content in navigation
3. Re-index the vector store (if needed for search)

### Adding New API Endpoints

1. Create the endpoint in `backend/api/endpoints/`
2. Add the router to `backend/main.py`
3. Update API documentation
4. Add tests

### Modifying the Chatbot Logic

1. Update logic in `backend/rag/chatbot.py`
2. Consider updating prompt templates
3. Test with various queries
4. Update response validation if needed

## Troubleshooting

### Common Issues

#### Backend Won't Start
- Check that the virtual environment is activated
- Verify all dependencies are installed
- Check for port conflicts (default: 8000)

#### Frontend Won't Start
- Ensure Node.js and npm are properly installed
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

#### Vector Store Issues
- Check that the index files exist
- Verify the docs path is correct
- Re-index if documents have changed significantly

#### Embedding Model Won't Load
- Ensure internet connectivity for initial download
- Check available disk space in Hugging Face cache
- Verify the model name is correct

### Performance Tips

- Use a virtual environment to avoid dependency conflicts
- Keep the vector store updated with current content
- Monitor memory usage during indexing
- Use GPU acceleration if available for faster embeddings

## Contributing

### Code Standards

- Follow PEP 8 for Python code
- Use TypeScript for type safety in frontend
- Write comprehensive docstrings
- Include unit tests for new functionality
- Follow the existing code style

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests if applicable
4. Update documentation if needed
5. Run all tests to ensure nothing is broken
6. Submit a pull request with a clear description

## Getting Help

If you encounter issues:

1. Check the existing GitHub issues
2. Review the documentation
3. Ask questions in the project's communication channels
4. Create a new issue with detailed information about the problem