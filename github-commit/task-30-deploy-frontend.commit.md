# GitHub Commit: Task 30 - Deploy Frontend (GitHub Pages/Vercel)

**Date**: 2025-12-07T23:14:50+05:00
**Type**: Task Execution

## Commit Title
ci: configure github pages deployment for frontend

## Summary
Updated Docusaurus configuration with repository details and added a GitHub Actions workflow to automate the build and deployment process.

## Task Number
30

## Files Modified
- `frontend/docusaurus.config.ts`
- `.github/workflows/deploy.yml` (New)
- `tasks.md`

## Why Change Was Needed
To enable continuous delivery of the textbook website to the public internet via GitHub Pages.

## Git Commit Command
```bash
git add frontend/docusaurus.config.ts .github/workflows/deploy.yml tasks.md
git commit -m "ci: configure github pages deployment for frontend"
```

## Git Commit Description
```text
Configure Frontend Deployment

- Set production URL and BaseURL in Docusaurus config
- Create GH Actions workflow for automated build/deploy
- Target gh-pages branch for static site hosting
```
