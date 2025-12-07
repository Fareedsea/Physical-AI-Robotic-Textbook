# GitHub Commit: Task 24 - Build Floating Chatbot Component

**Date**: 2025-12-07T22:55:05+05:00
**Type**: Task Execution

## Commit Title
feat: add floating chatbot ui component

## Summary
Implemented the frontend UI for the global chatbot assistant, including a floating toggle button, expandable window, and basic layout structure.

## Task Number
24

## Files Modified
- `frontend/src/components/Chatbot/index.tsx` (New)
- `frontend/src/components/Chatbot/styles.module.css` (New)
- `frontend/src/theme/Root.tsx`
- `tasks.md`

## Why Change Was Needed
To provide the user interface for the AI assistant that will eventually connect to the RAG backend.

## Git Commit Command
```bash
git add frontend/src/components/Chatbot/ frontend/src/theme/Root.tsx tasks.md
git commit -m "feat: add floating chatbot ui component"
```

## Git Commit Description
```text
Build Floating Chatbot Component

- Create Chatbot React component with open/close state
- Implement CSS modules for styling (floating FAB, window animations)
- Inject Chatbot globally via Docusaurus Root wrapper
```
