# GitHub Commit: Task 23 - Create Query API Endpoints

**Date**: 2025-12-07T22:51:50+05:00
**Type**: Task Execution

## Commit Title
feat: implement query api endpoints with rag and selection support

## Summary
Added the final RAG API layer, enabling the chatbot to answer questions using retrieved textbook context or user-selected text segments.

## Task Number
23

## Files Modified
- `backend/rag/query.py` (New)
- `backend/main.py`
- `tasks.md`

## Why Change Was Needed
To power the "Ask AI" and "Explain this Selection" features in the frontend, completing the backend's core RAG responsibilities.

## Git Commit Command
```bash
git add backend/rag/query.py backend/main.py tasks.md
git commit -m "feat: implement query api endpoints with rag and selection support"
```

## Git Commit Description
```text
Implement Query API Endpoints

- Add QueryRequest and SelectedTextQueryRequest models
- Implement generate_answer using OpenAI GPT-4o
- Add /query endpoint for full RAG search
- Add /query-selected endpoint for focused explanations
```
