# Data Model: UI Theme and Navigation Structure

## UI Theme Entity

### Definition
The UI Theme entity represents the visual styling configuration that defines the appearance of the Docusaurus textbook website.

### Attributes
- **primaryBackground** (string): Primary background color value (e.g., "#1a1a1a" for deep charcoal)
- **secondaryBackground** (string): Secondary background color for contrast areas (e.g., "#2a2a2a")
- **accentColor** (string): Primary accent color (e.g., "#00b4d8" for electric blue)
- **secondaryAccent** (string): Secondary accent color (e.g., "#00f5d4" for cyan)
- **tertiaryAccent** (string): Tertiary accent color (e.g., "#7209b7" for violet)
- **textPrimary** (string): Primary text color (e.g., "#e6e6e6" for light gray)
- **textSecondary** (string): Secondary text color (e.g., "#c2c2c2")
- **textMuted** (string): Muted text color for less important information (e.g., "#a0a0a0")
- **borderColor** (string): Border color for UI elements
- **codeBlockTheme** (object): Configuration for code block syntax highlighting
- **contrastRatio** (number): WCAG compliance value (minimum 4.5 for normal text)

### Relationships
- Applied to all pages and components of the website
- Influences all Docusaurus theme components
- Affects all content rendering elements

### Validation Rules
- All color combinations must meet WCAG 2.1 AA accessibility standards
- Contrast ratio between text and background must be ≥ 4.5:1 for normal text
- Theme configuration must be compatible with Docusaurus theming system

## Navigation Structure Entity

### Definition
The Navigation Structure entity represents the organization and labeling of the textbook's navigation system, ensuring consistent terminology across UI elements.

### Attributes
- **navbarLabel** (string): Label displayed in the main navigation bar (e.g., "Chapters")
- **sidebarLabels** (array<string>): Labels used in the sidebar navigation
- **breadcrumbLabels** (array<string>): Labels used in breadcrumb navigation
- **routeMappings** (object): Mapping of navigation items to content routes
- **activeStates** (object): Configuration for highlighting current page
- **hierarchyLevels** (number): Number of levels in the navigation hierarchy
- **mobileBehavior** (object): Configuration for mobile navigation behavior

### Relationships
- Connects to the site's content structure
- Influences user navigation patterns
- Affects SEO and site organization

### Validation Rules
- All navigation routes must remain unchanged from current implementation
- Labels must be consistent across navbar, sidebar, and breadcrumbs
- Navigation structure must maintain accessibility standards
- Mobile navigation must be touch-friendly and responsive

## Typography Configuration Entity

### Definition
The Typography Configuration entity defines the text styling rules that enhance readability and visual hierarchy.

### Attributes
- **baseFontSize** (string): Base font size for body text (e.g., "16px")
- **lineHeight** (number): Line height multiplier for readability (e.g., 1.7)
- **headingScale** (object): Size scale for h1-h6 elements
- **fontFamily** (string): Font family stack for body text
- **fontWeightNormal** (number): Normal text weight
- **fontWeightBold** (number): Bold text weight
- **paragraphSpacing** (string): Vertical spacing between paragraphs

### Relationships
- Applied to all content pages
- Affects readability of all text content
- Influences code block presentation

### Validation Rules
- Line height must enhance readability without excessive spacing
- Heading hierarchy must be visually distinct
- Font sizes must be responsive across device sizes