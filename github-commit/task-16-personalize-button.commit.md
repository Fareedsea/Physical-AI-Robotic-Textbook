# GitHub Commit: Task 16 - Implement Personalize Content Button

**Date**: 2025-12-07T22:30:15+05:00
**Type**: Task Execution

## Commit Title
feat: implement personalize content button in doc header

## Summary
Added a global "Personalize Content" button to all documentation pages by wrapping the Docusaurus DocItem/Content component.

## Task Number
16

## Files Modified
- `frontend/src/components/PersonalizeButton/index.tsx` (New)
- `frontend/src/components/PersonalizeButton/styles.module.css` (New)
- `frontend/src/theme/DocItem/Content/index.tsx` (New)
- `tasks.md`

## Why Change Was Needed
To allow users to toggle "Personalized Mode" for the textbook content, adjusting the difficulty or focus based on their profile (e.g., Software vs Hardware background).

## Git Commit Command
```bash
git add frontend/src/components/PersonalizeButton/ frontend/src/theme/DocItem/Content/ tasks.md
git commit -m "feat: implement personalize content button in doc header"
```

## Git Commit Description
```text
Implement Personalize Content Button

- Create PersonalizeButton component connected to AuthContext
- Swizzle DocItem/Content to inject button globally
- Add styles for personalization state
```
