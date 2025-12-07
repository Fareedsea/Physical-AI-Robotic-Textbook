# GitHub Commit: Task 21 - Implement Document Ingestion API

**Date**: 2025-12-07T22:45:10+05:00
**Type**: Task Execution

## Commit Title
feat: implement document ingestion api

## Summary
Added the `/ingest` API endpoint and underlying logic to accept and chunk text documents, preparing them for the RAG embedding pipeline.

## Task Number
21

## Files Modified
- `backend/rag/ingest.py` (New)
- `backend/main.py`
- `tasks.md`

## Why Change Was Needed
To allow the system to process textbook content and user documents for the vector search engine.

## Git Commit Command
```bash
git add backend/rag/ingest.py backend/main.py tasks.md
git commit -m "feat: implement document ingestion api"
```

## Git Commit Description
```text
Implement Document Ingestion API

- Create IngestRequest model using Pydantic
- Implement text chunking utility (sliding window)
- Add POST /ingest endpoint to FastAPI app
```
