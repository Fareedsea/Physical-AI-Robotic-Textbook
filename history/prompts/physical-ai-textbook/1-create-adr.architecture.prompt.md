---
id: 1
title: Create ADR
stage: architecture
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: physical-ai-textbook
branch: 001-physical-ai-textbook
user: user
command: /sp.adr
labels: [architecture, decision-record, textbook]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  plan: specs/001-physical-ai-textbook/plan.md
  research: specs/001-physical-ai-textbook/research.md
  data-model: specs/001-physical-ai-textbook/data-model.md
  adr: history/adr/001-physical-ai-textbook-architecture.md
  contracts: specs/001-physical-ai-textbook/contracts/chatbot-api.yaml
  ticket: null
  pr: null
files:
  - history/adr/001-physical-ai-textbook-architecture.md
tests:
  - none
---

## Prompt

/sp.adr Physical-AI-Textbook-Architecture

## Response snapshot

# ADR-001: Physical AI & Humanoid Robotics Textbook Architecture

**Status:** Accepted
**Date:** 2025-12-10

## Context

The Physical AI & Humanoid Robotics Textbook project requires a robust, scalable architecture that supports educational content delivery, interactive learning through a RAG chatbot, and integration with robotics frameworks (ROS 2, Gazebo, NVIDIA Isaac, VLA). The system must be accessible via GitHub Pages while maintaining high performance for both static content delivery and dynamic AI interactions.

Key constraints include:
- Must follow Docusaurus Markdown format for GitHub Pages deployment
- Need to integrate ROS 2, Gazebo, NVIDIA Isaac, and VLA concepts
- Target 1000+ students accessing content
- 85% accuracy for RAG chatbot responses
- Pages load in <2 seconds, RAG responses in <3 seconds for 95% of queries

## Decision

We have adopted a **hybrid architecture** with:

### Frontend: Docusaurus Documentation Site
- **Framework**: Docusaurus v3.x with React and TypeScript
- **Content Format**: Markdown following Docusaurus standards
- **Deployment**: GitHub Pages for static content hosting
- **Styling**: Custom CSS with responsive design
- **Navigation**: Structured sidebar with 10 textbook chapters

### Backend: FastAPI RAG Service
- **Framework**: FastAPI with Python 3.9+
- **RAG Implementation**: LangChain + FAISS for vector storage
- **API**: RESTful endpoints for chat and content search
- **Model Integration**: Support for multiple LLM providers
- **Testing**: pytest for backend components

### Data Architecture
- **Content Storage**: Markdown files in Docusaurus docs structure
- **Vector Storage**: FAISS index for textbook content embeddings
- **Session Management**: In-memory storage for user sessions
- **Content Indexing**: Document chunking with metadata preservation

### Integration Architecture
- **Frontend-Backend**: API calls from Docusaurus to FastAPI backend
- **Chat Interface**: React component integrated into textbook pages
- **Source Citations**: Direct linking from chat responses to textbook content
- **Authentication**: Optional session-based tracking

## Alternatives Considered

### Alternative 1: Full Custom React Application
- **Approach**: Build complete custom React application with routing
- **Pros**: Maximum flexibility, custom UI/UX, better integration
- **Cons**: More complex development, harder deployment, more maintenance

### Alternative 2: Static Site with Client-Side AI
- **Approach**: Run AI models directly in browser using ONNX.js or similar
- **Pros**: No backend required, better privacy, simpler deployment
- **Cons**: Performance limitations, model size constraints, limited functionality

### Alternative 3: Headless CMS Approach
- **Approach**: Use headless CMS (Strapi, Contentful) for content management
- **Pros**: Better content management, user-friendly editor, versioning
- **Cons**: Additional costs, external dependency, complexity

### Alternative 4: Server-Side Rendering (Next.js)
- **Approach**: Use Next.js with SSR for better SEO and performance
- **Pros**: Better performance, SEO optimization, full-stack framework
- **Cons**: More complex deployment, higher resource usage, steeper learning curve

## Consequences

### Positive Consequences
- **Scalability**: GitHub Pages provides excellent scalability for static content
- **Performance**: Docusaurus optimized for documentation sites with fast loading
- **Maintainability**: Clear separation between content and logic
- **Community**: Strong ecosystem and community support for both technologies
- **Cost-Effective**: Free hosting with GitHub Pages
- **Offline Access**: PWA capabilities for offline reading
- **Integration**: Easy to add new robotics frameworks and tools

### Negative Consequences
- **Backend Dependency**: RAG chatbot requires separate backend service
- **Deployment Complexity**: Two separate deployment processes
- **Learning Curve**: Team needs to learn both Docusaurus and FastAPI
- **Caching**: Static content updates require rebuild and redeployment
- **Security**: API endpoints need proper authentication and rate limiting

## References

- `specs/001-physical-ai-textbook/plan.md` - Implementation plan with technical context
- `specs/001-physical-ai-textbook/research.md` - Research findings on technology decisions
- `specs/001-physical-ai-textbook/data-model.md` - Data models for content and user interactions
- `specs/001-physical-ai-textbook/contracts/chatbot-api.yaml` - API contract specification

## Outcome

- ✅ Impact: Created comprehensive ADR documenting the Physical AI textbook architecture
- 🧪 Tests: none
- 📁 Files: Created ADR-001 documenting the hybrid architecture approach
- 🔁 Next prompts: Continue with development based on documented architecture
- 🧠 Reflection: ADR captures key architectural decisions with alternatives and consequences

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A