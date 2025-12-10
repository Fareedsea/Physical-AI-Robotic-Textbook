// tests/integration/deployment.test.js
// GitHub Pages deployment test

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

describe('GitHub Pages Deployment Test', () => {
  test('Docusaurus build completes successfully', () => {
    // Verify that the build command runs without errors
    expect(() => {
      execSync('cd my-website && npm run build', { stdio: 'pipe' });
    }).not.toThrow();
  });

  test('Build output directory exists after build', () => {
    const buildDir = path.join(__dirname, '../../my-website/build');
    expect(fs.existsSync(buildDir)).toBe(true);
  });

  test('Build output contains expected files', () => {
    const buildDir = path.join(__dirname, '../../my-website/build');
    const expectedFiles = ['index.html', 'assets'];

    expectedFiles.forEach(file => {
      expect(fs.existsSync(path.join(buildDir, file))).toBe(true);
    });
  });

  test('Static assets are properly generated', () => {
    const buildDir = path.join(__dirname, '../../my-website/build');
    const assetsDir = path.join(buildDir, 'assets');

    if (fs.existsSync(assetsDir)) {
      const files = fs.readdirSync(assetsDir);
      expect(files.length).toBeGreaterThan(0);
    }
  });
});