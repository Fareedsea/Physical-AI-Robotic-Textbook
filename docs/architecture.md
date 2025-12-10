# Architecture Overview

## System Architecture

The Physical AI & Humanoid Robotics Textbook follows a modern, scalable architecture with clear separation of concerns between frontend, backend, and data layers.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Frontend Layer                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │   Docusaurus    │  │   React Chatbot  │  │      API Client              │   │
│  │   Static Site   │  │      UI          │  │    (JavaScript)              │   │
│  │                 │  │                  │  │                              │   │
│  │ - Textbook      │  │ - Q&A Interface  │  │ - REST API Communication     │   │
│  │   Content       │  │ - Source Citations│ │ - Session Management         │   │
│  │ - Navigation    │  │ - Feedback       │  │ - Error Handling             │   │
│  │ - Search        │  │   Collection     │  │                              │   │
│  └─────────────────┘  └──────────────────┘  └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Backend Layer                                      │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │   FastAPI       │  │   RAG Core       │  │   Integration Modules        │   │
│  │   Web Server    │  │   Services       │  │                              │   │
│  │                 │  │                  │  │ ┌──────────────────────────┐ │   │
│  │ - API Routes    │  │ - Chatbot        │  │ │     ROS 2 Module         │ │   │
│  │ - Authentication│  │ - Search         │  │ │     Gazebo Module        │ │   │
│  │ - Rate Limiting │  │ - Indexing       │  │ │     Isaac Module         │ │   │
│  │ - Logging       │  │ - Validation     │  │ │     VLA Module           │ │   │
│  └─────────────────┘  └──────────────────┘  │ └──────────────────────────┘ │   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Data Layer                                         │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │   Vector Store  │  │   Document       │  │   Session Storage            │   │
│  │   (FAISS)       │  │   Storage        │  │                              │   │
│  │                 │  │                  │  │ ┌──────────────────────────┐ │   │
│  │ - Embeddings    │  │ - Textbook       │  │ │    In-Memory Store       │ │   │
│  │ - Similarity    │  │   Markdown       │  │ │    File-Based Store      │ │   │
│  │   Search        │  │ - Metadata       │  │ └──────────────────────────┘ │   │
│  │ - Indexing      │  │ - Structure      │  │                              │   │
│  └─────────────────┘  └──────────────────┘  └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Components

#### Docusaurus Static Site
- **Purpose**: Hosts textbook content and provides navigation
- **Technology**: React-based static site generator
- **Features**:
  - Markdown-based content management
  - Responsive design
  - Built-in search
  - Multi-language support

#### React Chatbot UI
- **Purpose**: Provides interactive Q&A interface
- **Technology**: React with hooks
- **Features**:
  - Real-time conversation
  - Source citation display
  - Confidence scoring
  - Feedback collection
  - Session persistence

#### API Client
- **Purpose**: Handles communication with backend APIs
- **Technology**: JavaScript/TypeScript
- **Features**:
  - REST API communication
  - Error handling
  - Request/response formatting

### Backend Components

#### FastAPI Web Server
- **Purpose**: Handles HTTP requests and serves APIs
- **Technology**: FastAPI with Python
- **Features**:
  - Automatic API documentation (Swagger UI)
  - Request validation
  - Dependency injection
  - Asynchronous processing

#### RAG Core Services
- **Purpose**: Implements Retrieval-Augmented Generation functionality
- **Technology**: Python with LangChain
- **Features**:
  - Document indexing and retrieval
  - Vector similarity search
  - Response generation
  - Content validation

#### Integration Modules
- **Purpose**: Provides interfaces to robotics frameworks
- **Technology**: Python with specialized libraries
- **Features**:
  - ROS 2 integration
  - Gazebo simulation
  - NVIDIA Isaac
  - Vision-Language-Action systems

### Data Components

#### Vector Store (FAISS)
- **Purpose**: Stores document embeddings for similarity search
- **Technology**: FAISS (Facebook AI Similarity Search)
- **Features**:
  - Fast similarity search
  - Multiple distance metrics
  - Index persistence

#### Document Storage
- **Purpose**: Stores original textbook content
- **Technology**: File system (Markdown files)
- **Features**:
  - Version control friendly
  - Human-readable format
  - Easy to edit

#### Session Storage
- **Purpose**: Maintains conversation state
- **Technology**: In-memory or file-based storage
- **Features**:
  - User session tracking
  - Conversation history
  - Message persistence

## API Architecture

### REST API Design

The backend provides a RESTful API with the following endpoints:

```
/api/
├── /chat/
│   ├── POST /query          # Query the chatbot
│   ├── GET /history         # Get conversation history
│   └── POST /feedback       # Submit feedback
└── /content/
    ├── POST /search         # Search textbook content
    └── GET /search          # Simple search
```

### Data Flow

1. **User Request**: Frontend sends request to backend
2. **Request Validation**: FastAPI validates input
3. **Processing**: Appropriate service handles request
4. **Data Retrieval**: Services access vector store/documents
5. **Response Generation**: Services generate response
6. **Response Validation**: Response is validated
7. **Return**: Response is returned to frontend

## Security Architecture

### Authentication & Authorization
- API rate limiting
- Input validation
- Secure communication (HTTPS)

### Data Protection
- Vector store encryption (optional)
- Session management
- Access logging

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Distributed vector store (future enhancement)
- Caching layer (future enhancement)

### Performance Optimization
- Efficient vector search
- Response caching
- Asynchronous processing

## Deployment Architecture

### Production Deployment
- Static site hosting (GitHub Pages)
- Backend server (containerized)
- CDN for static assets
- Load balancing (future enhancement)

### Development Environment
- Local development server
- Hot reloading
- Development database
- Local vector store