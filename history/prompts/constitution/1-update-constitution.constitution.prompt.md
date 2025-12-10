---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

## Response snapshot

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Technical Accuracy
All technical concepts must match real-world robotics systems including ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action (VLA) frameworks. This ensures students learn industry-standard tools and practices that directly apply to current robotics development workflows.

### II. Pedagogical Clarity
Content must prioritize beginner-to-intermediate clarity for students. Complex robotics concepts should be broken down into digestible explanations with clear examples that build understanding progressively from fundamentals to advanced applications.

### III. Practical Learning
Every module must include hands-on workflows and simulations that allow students to apply concepts immediately. Learning outcomes must be measurable through practical tasks rather than theoretical understanding alone.

### IV. AI-Native Integration
The curriculum must embrace AI-native thinking by integrating Large Language Models, Robotics, and Simulation in a unified learning approach. This reflects the current state of robotics development where AI plays a central role.

### V. Simple Language with Clear Examples
All content must use simple language with concrete examples that illustrate abstract concepts. Each module must include learning goals and applied outcomes to ensure measurable progress.

### VI. Docusaurus Markdown Standard
All content must be written in Docusaurus Markdown format to ensure proper deployment on GitHub Pages. This maintains consistency across the textbook and enables proper documentation site generation.

## Deployment Standards
Content must be structured for GitHub Pages deployment with integration of RAG chatbot capabilities. All technical concepts must align with ROS 2, Gazebo, NVIDIA Isaac, and VLA usage to ensure technical accuracy.

## Development Workflow
Content development follows the Spec-Kit Plus workflow: Constitution → Specify → Plan → Tasks → Implement. Each module must include key concepts, practical tasks, and measurable learning outcomes. All content must be written in English with potential for Urdu translation in the future.

## Governance
This constitution governs all development of the Physical AI & Humanoid Robotics Textbook. All content and implementation must comply with these principles. Amendments require documentation of changes and approval from project maintainers. The constitution supersedes any conflicting practices or guidelines.

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10

## Outcome

- ✅ Impact: Created initial project constitution for Physical AI & Humanoid Robotics Textbook
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: /sp.specify to create feature specification
- 🧠 Reflection: Constitution properly established with 6 core principles aligned to project goals

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A