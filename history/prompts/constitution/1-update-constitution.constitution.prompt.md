---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude
command: /sp.constitution
labels: [constitution, textbook, ai, robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/spec-template.md
 - .specify/templates/plan-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

## /sp.constitution

Project: Physical AI & Humanoid Robotics Textbook

Core Principles: - Clear and beginner-friendly explanations - Accurate
and verified technical content - Practical, real-world robotics
relevance - Consistent structure across all chapters - AI-native
learning design

Key Standards: - All technical claims must be verifiable - Writing
style: Simple, professional, and structured - No AI hallucinations
allowed - Each chapter must include: - Introduction - Core Concepts -
Practical Example - Summary

Constraints: - Format: Markdown (.md) - Platform: Docusaurus -
Deployment: GitHub Pages - Toolchain: Spec-Kit Plus + Claude Code -
Target Audience: Beginners to intermediate learners - Plagiarism: 0%
tolerance - No copyrighted content

Success Criteria: - Book builds successfully in Docusaurus - GitHub
Pages deployment works correctly - Content is accurate, clear, and
reproducible - The book serves as a complete self-learning resource

## Response snapshot

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Clear and Beginner-Friendly Explanations
All content must be accessible to beginners with no prior robotics or AI knowledge; explanations should use simple language, analogies, and step-by-step guidance; complex concepts must be broken down into digestible parts with clear learning progressions.

### II. Accurate and Verified Technical Content
All technical claims must be verifiable through authoritative sources or practical implementation; content must be fact-checked and validated before publication; any theoretical concepts must be supported by real-world applications or proven research.

### III. Practical, Real-World Robotics Relevance
Content must connect directly to real-world robotics applications; examples and exercises should reflect actual robotics challenges and solutions; focus on skills and knowledge that have practical utility in robotics development.

### IV. Consistent Structure Across All Chapters
Each chapter must follow the standardized structure: Introduction → Core Concepts → Practical Example → Summary; consistent formatting, terminology, and pedagogical approach across all chapters; maintain uniform learning experience throughout the textbook.

### V. AI-Native Learning Design
Content must leverage AI tools and methodologies for enhanced learning; incorporate interactive elements and AI-assisted learning features; design for AI-powered study aids and automated feedback systems.

## Content Standards
All technical claims must be verifiable; writing style must be simple, professional, and structured; no AI hallucinations allowed; each chapter must include: Introduction, Core Concepts, Practical Example, Summary; all content must be original with 0% plagiarism tolerance.

## Technical Constraints
Format: Markdown (.md); Platform: Docusaurus; Deployment: GitHub Pages; Toolchain: Spec-Kit Plus + Claude Code; Target Audience: Beginners to intermediate learners; No copyrighted content allowed; Strict adherence to ethical AI practices.

## Success Criteria
Book builds successfully in Docusaurus; GitHub Pages deployment works correctly; Content is accurate, clear, and reproducible; The book serves as a complete self-learning resource; All chapters meet the defined structure and quality standards.

## Governance
This constitution governs all content creation and technical decisions for the Physical AI & Humanoid Robotics Textbook project; All contributions must comply with these principles; Amendments require documentation and approval through the project's standard review process; All PRs and reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07

## Outcome

- ✅ Impact: Updated constitution to reflect Physical AI & Humanoid Robotics Textbook project principles
- 🧪 Tests: none
- 📁 Files: Updated constitution.md and aligned templates (spec, plan, tasks)
- 🔁 Next prompts: Continue with project implementation
- 🧠 Reflection: Constitution now properly reflects the textbook project requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none