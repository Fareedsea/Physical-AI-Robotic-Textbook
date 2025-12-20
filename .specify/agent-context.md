# Physical AI & Humanoid Robotics Textbook Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-19

## Active Technologies

- Docusaurus v2+
- React
- CSS/SCSS
- Node.js
- Markdown
- TypeScript (for configuration)

## Project Structure

```text
my-website/
├── docusaurus.config.ts
├── src/css/custom.css
├── sidebars.js
├── docs/
└── package.json

specs/002-docusaurus-ui-upgrade/
├── spec.md
├── plan.md
├── plan/research.md
├── plan/data-model.md
├── plan/quickstart.md
└── checklists/
```

## Commands

- `npm run start` - Start development server (my-website directory)
- `npm run build` - Build static site
- `npm run serve` - Serve built site locally
- Edit `docusaurus.config.ts` for navigation and site configuration
- Edit `src/css/custom.css` for custom styling
- Use browser dev tools for responsive testing

## Code Style

- Follow Docusaurus theming best practices
- Use CSS custom properties for theming
- Maintain accessibility standards (WCAG 2.1 AA)
- Use semantic HTML and proper heading hierarchy
- Follow existing code formatting in the project

## Recent Changes

- Feature 001: Physical AI Textbook - Initial textbook structure and content
- Feature 002: Docusaurus UI Upgrade - Dark theme implementation, navigation improvements, responsive design

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->