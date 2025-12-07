# GitHub Commit: Task 17 - Implement Translate to Urdu Button

**Date**: 2025-12-07T22:33:50+05:00
**Type**: Task Execution

## Commit Title
feat: implement translate to urdu button

## Summary
Added a "Translate to Urdu" toggle button to the documentation header, sitting alongside the Personalize button.

## Task Number
17

## Files Modified
- `frontend/src/components/TranslateButton/index.tsx` (New)
- `frontend/src/components/TranslateButton/styles.module.css` (New)
- `frontend/src/theme/DocItem/Content/index.tsx`
- `tasks.md`

## Why Change Was Needed
To support multilingual accessibility, specifically enabling Urdu translation for the textbook content as per project requirements.

## Git Commit Command
```bash
git add frontend/src/components/TranslateButton/ frontend/src/theme/DocItem/Content/index.tsx tasks.md
git commit -m "feat: implement translate to urdu button"
```

## Git Commit Description
```text
Implement Translate to Urdu Button

- Create TranslateButton component with simulated toggle logic
- Integrate into DocItem/Content wrapper next to Personalize button
- Enhance documentation header layout
```
