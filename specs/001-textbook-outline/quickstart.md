# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Overview

This guide provides a quick path to get started with developing the Physical AI & Humanoid Robotics textbook. The textbook follows a structured approach with each chapter containing Introduction → Core Concepts → Practical Example → Summary sections.

## Prerequisites

- Git installed on your system
- Node.js (version 16 or higher) for Docusaurus
- Basic understanding of Markdown syntax
- Access to authoritative sources for technical verification

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start local development server**
   ```bash
   npm start
   ```
   This will start a local server at `http://localhost:3000` with hot reloading.

## Creating a New Chapter

1. **Create the chapter directory**
   ```
   docs/chapter-n-<topic-name>/
   ```

2. **Add the required files**:
   - `index.md` - Chapter introduction and learning objectives
   - `core-concepts.md` - Core concepts section
   - `practical-example.md` - Practical example section
   - `summary.md` - Chapter summary

3. **Follow the content structure**:
   - Each section should be beginner-friendly
   - Include practical examples that connect to real-world robotics
   - Ensure all technical claims are verifiable
   - Add learning objectives at the beginning

## Content Guidelines

### Writing Style
- Use simple, professional language
- Explain complex concepts in digestible parts
- Include analogies where appropriate
- Maintain consistent terminology

### Technical Accuracy
- Verify all technical claims with authoritative sources
- Include references to academic papers or official documentation
- Mark uncertain information for review
- Update content as the field evolves

### Structure Requirements
- Each chapter must follow: Introduction → Core Concepts → Practical Example → Summary
- Include learning objectives for each chapter
- Add practical examples that demonstrate real-world applications
- Create summaries that reinforce key concepts

## Building and Deployment

1. **Build the static site**
   ```bash
   npm run build
   ```

2. **Serve the built site locally for testing**
   ```bash
   npm run serve
   ```

3. **Deployment** is handled automatically via GitHub Actions when changes are pushed to the main branch.

## Review Process

1. **Content verification**: Ensure all technical claims are accurate
2. **Beginner accessibility**: Verify content is suitable for beginners
3. **Structure compliance**: Check that all chapters follow the required format
4. **Plagiarism check**: Ensure all content is original
5. **Peer review**: Subject matter experts review content for accuracy

## Common Tasks

### Adding Images or Diagrams
- Place images in the `static/img/` directory
- Reference them in Markdown as: `![Alt text](/img/image-name.png)`

### Adding New Glossary Terms
- Add terms to the `docs/glossary.md` file
- Include clear, concise definitions
- Link to authoritative sources where possible

### Updating Navigation
- Modify `sidebars.js` to update the site navigation
- Organize chapters in the correct learning progression order

## Troubleshooting

- **Build errors**: Check that all Markdown files have proper formatting
- **Missing content**: Verify all required sections are present in each chapter
- **Link errors**: Ensure all internal links use the correct paths
- **Search not working**: Verify that Docusaurus is properly configured