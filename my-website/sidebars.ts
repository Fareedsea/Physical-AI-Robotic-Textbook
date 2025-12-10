import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar for our textbook structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 1: Basics of Physical AI',
      items: ['chapter-1-basics-physical-ai/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 2: Robotics Foundations',
      items: ['chapter-2-robotics-foundations/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 3: Humanoid Systems',
      items: ['chapter-3-humanoid-systems/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 4: Sensors and Actuators',
      items: ['chapter-4-sensors-actuators/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 5: Control Systems',
      items: ['chapter-5-control-systems/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 6: Perception and Vision',
      items: ['chapter-6-perception-vision/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 7: Machine Learning for Robots',
      items: ['chapter-7-machine-learning-robots/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 8: Human-Robot Interaction',
      items: ['chapter-8-human-robot-interaction/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 9: Safety and Ethics',
      items: ['chapter-9-safety-ethics/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapter 10: Real-World Applications',
      items: ['chapter-10-real-world-applications/intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Appendices',
      items: ['glossary', 'references'],
      collapsed: true,
    }
  ],
};

export default sidebars;
