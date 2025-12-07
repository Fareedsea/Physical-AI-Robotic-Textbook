# GitHub Commit: Task 26 - Connect Chatbot to Backend API

**Date**: 2025-12-07T23:01:45+05:00
**Type**: Task Execution

## Commit Title
feat: connect frontend chatbot to fastapi backend

## Summary
Replaced the mock chat logic with a real HTTP integration, sending user queries to the FastAPI RAG endpoint to generate intelligent responses.

## Task Number
26

## Files Modified
- `frontend/src/components/Chatbot/index.tsx`
- `tasks.md`

## Why Change Was Needed
To enable actual AI functionality by connecting the user interface to the intelligence engine (Backend/RAG).

## Git Commit Command
```bash
git add frontend/src/components/Chatbot/index.tsx tasks.md
git commit -m "feat: connect frontend chatbot to fastapi backend"
```

## Git Commit Description
```text
Connect Chatbot to Backend API

- Replace mock timeout with fetch POST /query
- Serialize conversation history for context awareness
- Add error handling for failed API requests
```
