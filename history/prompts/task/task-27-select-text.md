# History Log: Task 27 - Implement "Ask AI on Selected Text"

**Date**: 2025-12-07T23:05:20+05:00
**Type**: Task Execution

## Prompt
"continue task" (Proceed with Task 27)

## Work Performed
1. Re-read specifications.
2. Created `frontend/src/components/SelectionTooltip/index.tsx`:
   - Utilized `window.getSelection()`/`mouseup` to detect highlights.
   - Implemented dynamic positioning logic to place button above text.
   - Dispatched `ASK_AI_SELECTION` custom event.
3. Created `frontend/src/components/SelectionTooltip/styles.module.css`.
4. Updated `frontend/src/theme/Root.tsx` to include `SelectionTooltip`.
5. Updated `frontend/src/components/Chatbot/index.tsx`:
   - Added event listener for `ASK_AI_SELECTION`.
   - Implemented `handleSendSelection` to call `/query-selected` API.

## Outcome
Users can now highlight any text in the textbook, click "Ask AI", and instantly see the Chatbot pop up with an explanation of that specific text.
