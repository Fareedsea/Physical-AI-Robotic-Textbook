# History Log: Task 26 - Connect Chatbot to Backend API

**Date**: 2025-12-07T23:01:45+05:00
**Type**: Task Execution

## Prompt
"continue task" (Proceed with Task 26)

## Work Performed
1. Re-read specifications.
2. Updated `frontend/src/components/Chatbot/index.tsx`:
   - Replaced simulated `setTimeout` logic with real `fetch` call to `http://localhost:8000/query`.
   - Constructed `historyForApi` payload.
   - Implemented error handling for network errors (displaying a user-friendly message).
   - Parsed the JSON response to display `data.answer`.
3. Updated `tasks.md`.

## Outcome
The Chatbot is now "live". If the backend server is running (with Qdrant and OpenAI configured), the chatbot will provide intelligent answers based on the textbook content.
