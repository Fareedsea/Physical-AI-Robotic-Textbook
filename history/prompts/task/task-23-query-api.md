# History Log: Task 23 - Create Query API Endpoints

**Date**: 2025-12-07T22:51:50+05:00
**Type**: Task Execution

## Prompt
"continue task" (Proceed with Task 23)

## Work Performed
1. Re-read specifications.
2. Created `backend/rag/query.py`:
   - Defined `QueryRequest` and `SelectedTextQueryRequest` models.
   - Implemented `generate_answer` using OpenAI ChatCompletion.
   - Created `process_query` (RAG-based) and `process_selected_query` (Selection-based).
3. Updated `backend/main.py`:
   - Added `/query` and `/query-selected` POST endpoints.
4. Updated `tasks.md`.

## Outcome
The backend now fully supports the Chatbot logic: users can ask general questions (contextualized by the vector DB) or ask questions specific to text they've highlighted in the book.
