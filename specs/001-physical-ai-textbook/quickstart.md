# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Overview
This guide provides a quick start for developers to set up, develop, and deploy the Physical AI & Humanoid Robotics Textbook project.

## Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+
- Git
- GitHub account for deployment

## Setup Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Docusaurus Frontend
```bash
# Navigate to the website directory
cd my-website

# Install dependencies
npm install
# or
yarn install

# Start development server
npm start
# or
yarn start
```

The development server will start at `http://localhost:3000`.

### 3. Set up Backend for RAG Chatbot
```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn main:app --reload
```

## Content Development

### Adding New Chapters
1. Create a new markdown file in `my-website/docs/`
2. Follow the Docusaurus markdown format
3. Add the new chapter to `my-website/sidebars.js`

Example chapter structure:
```markdown
---
title: Chapter Title
sidebar_position: 1
---

# Chapter Title

## Learning Objectives
- Objective 1
- Objective 2

## Introduction
Content here...

## Section Title
More content...
```

### Adding Interactive Elements
Docusaurus supports React components within markdown files:

```markdown
import ComponentName from '@site/src/components/ComponentName';

<ComponentName />
```

## RAG Chatbot Integration

### Indexing Textbook Content
```bash
# Run the document indexing script
python backend/rag/document_loader.py
```

### Testing the Chatbot API
```bash
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key concepts in Chapter 1?",
    "sessionId": "test-session"
  }'
```

## Running Tests

### Frontend Tests
```bash
cd my-website
npm test
# or
yarn test
```

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

## Building for Production

### Build Docusaurus Site
```bash
cd my-website
npm run build
# or
yarn build
```

The built site will be in the `my-website/build/` directory.

### Build Backend
```bash
cd backend
# Backend is Python-based and runs directly
# Ensure all dependencies are in requirements.txt
pip install -r requirements.txt
```

## Deployment

### GitHub Pages Deployment
The Docusaurus site is configured for GitHub Pages deployment:

1. Push changes to the `main` branch
2. GitHub Actions will automatically build and deploy the site
3. The site will be available at `https://<username>.github.io/<repository>`

### Backend Deployment (Optional)
For the RAG chatbot backend, you can deploy to:
- Heroku
- AWS
- Google Cloud
- Azure

Example deployment to Heroku:
```bash
heroku create
git push heroku main
heroku ps:scale web=1
```

## Development Workflow

### Content Creation
1. Create new content in `my-website/docs/`
2. Update `my-website/sidebars.js` to include new content in navigation
3. Test locally with `npm start`
4. Commit and push changes

### Feature Development
1. Create a new branch: `git checkout -b feature-name`
2. Implement the feature
3. Write tests
4. Run tests: `npm test` and `python -m pytest tests/`
5. Commit and create a pull request

### Content Review Process
1. All content should follow the pedagogical principles in the constitution
2. Each chapter must include learning objectives and outcomes
3. Practical exercises must be tested with simulation frameworks
4. Review for technical accuracy with ROS 2, Gazebo, NVIDIA Isaac, and VLA

## Troubleshooting

### Common Issues

**Docusaurus not starting:**
- Check Node.js version (must be 18+)
- Clear cache: `npm start -- --clear-cache`

**Python dependencies not installing:**
- Ensure Python 3.9+ is installed
- Update pip: `pip install --upgrade pip`

**API calls failing:**
- Verify backend server is running
- Check CORS configuration in backend settings

### Useful Commands

```bash
# Check Node.js version
node --version

# Check Python version
python --version

# Check Git status
git status

# Format code
npm run format  # for frontend
black .         # for Python backend
```

## Next Steps

1. Review the [full documentation](./spec.md) for detailed specifications
2. Check the [tasks list](./tasks.md) for current development priorities
3. Explore the [data model](./data-model.md) for content structure details
4. Review the [API contracts](./contracts/) for integration points