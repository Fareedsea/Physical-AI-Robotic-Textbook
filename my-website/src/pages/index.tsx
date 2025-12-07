import type {ReactNode} from 'react';
import { useState } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Define chapter data type
type Chapter = {
  id: string;
  title: string;
  position: number;
  summary: string;
};

// Chapter data - this would normally come from your docs directory
const chapters: Chapter[] = [
  {
    id: 'chapter-1-basics-physical-ai',
    title: 'Chapter 1: Basics of Physical AI',
    position: 1,
    summary: 'Introduction to Physical AI, the importance of embodiment in intelligent systems, key components of physical AI systems, and their relationship to humanoid robotics. This chapter establishes foundational concepts for understanding how intelligent systems interact with the physical world.'
  },
  {
    id: 'chapter-2-robotics-foundations',
    title: 'Chapter 2: Robotics Foundations',
    position: 2,
    summary: 'Explore the mechanical, electrical, and control systems that make Physical AI possible. Learn how robots are built, how they move, and how they interact with their environments through detailed examination of robotic components and systems.'
  },
  {
    id: 'chapter-3-humanoid-systems',
    title: 'Chapter 3: Humanoid Systems',
    position: 3,
    summary: 'Dive into humanoid robotics, examining the design principles, challenges, and applications of human-like robots. Understand how human-inspired form factors enable interaction with human-designed environments and tools.'
  },
  {
    id: 'chapter-4-sensors-actuators',
    title: 'Chapter 4: Sensors and Actuators',
    position: 4,
    summary: 'Learn about the sensory and motor systems that enable robots to perceive their environment and perform physical actions. Explore different types of sensors, actuators, and how they integrate with AI systems.'
  },
  {
    id: 'chapter-5-control-systems',
    title: 'Chapter 5: Control Systems',
    position: 5,
    summary: 'Understand the algorithms and architectures that enable robots to move and perform tasks. Covering feedback control, motion planning, and real-time control systems for robotic applications.'
  },
  {
    id: 'chapter-6-perception-vision',
    title: 'Chapter 6: Perception and Vision',
    position: 6,
    summary: 'Explore how robots perceive and interpret their environment through computer vision, sensor fusion, and pattern recognition techniques. Learn about object detection, scene understanding, and spatial awareness.'
  },
  {
    id: 'chapter-7-machine-learning-robots',
    title: 'Chapter 7: Machine Learning for Robots',
    position: 7,
    summary: 'Discover how machine learning algorithms enable robots to learn from experience, adapt to new situations, and improve their performance over time through reinforcement learning, imitation learning, and other approaches.'
  },
  {
    id: 'chapter-8-human-robot-interaction',
    title: 'Chapter 8: Human-Robot Interaction',
    position: 8,
    summary: 'Examine the principles and technologies that enable safe and effective interaction between humans and robots. Covering communication interfaces, social robotics, and collaborative robotics applications.'
  },
  {
    id: 'chapter-9-safety-ethics',
    title: 'Chapter 9: Safety and Ethics',
    position: 9,
    summary: 'Address critical safety considerations and ethical implications in Physical AI and robotics. Explore risk assessment, safety standards, and ethical frameworks for responsible AI deployment.'
  },
  {
    id: 'chapter-10-real-world-applications',
    title: 'Chapter 10: Real-World Applications',
    position: 10,
    summary: 'Survey practical applications of Physical AI and robotics across various industries including healthcare, manufacturing, service, and research. Understand implementation challenges and success stories.'
  }
];

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className="text--center">
          <Heading as="h1" className="hero__title">
            {siteConfig.title}
          </Heading>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.introduction}>
            <p className={styles.introText}>
              Welcome to the comprehensive guide on Physical AI and Humanoid Robotics. This textbook explores the fascinating intersection of artificial intelligence and physical systems, covering everything from fundamental concepts to advanced applications in humanoid robotics.
            </p>
            <p className={styles.introText}>
              Whether you're a student, researcher, or professional in the field, this resource provides in-depth knowledge on how AI systems can be embodied in physical forms to interact with and navigate the real world effectively.
            </p>
          </div>
        </div>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Reading - Physical AI Textbook 📚
          </Link>
          <Link
            className="button button--outline button--secondary button--lg"
            to="/docs/chapter-1-basics-physical-ai">
            Explore Chapters
          </Link>
        </div>
      </div>
    </header>
  );
}

// Chatbot component with state management
function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{id: number; text: string; sender: 'user' | 'bot'}[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user' as const
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend chat API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [{ role: 'user', content: inputValue }],
          context_text: null,
          temperature: 0.7
        })
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot' as const
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          text: 'Sorry, I encountered an error. Please try again.',
          sender: 'bot' as const
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
        sender: 'bot' as const
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {isOpen ? (
        <div className={styles.chatbotWindow}>
          <div className={styles.chatbotHeader}>
            <h4>AI Assistant</h4>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
            >
              ×
            </button>
          </div>
          <div className={styles.chatbotMessages}>
            {messages.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <p>Hello! I'm your AI assistant for the Physical AI and Robotics textbook. How can I help you today?</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`${styles.message} ${styles[message.sender]}`}
                >
                  {message.text}
                </div>
              ))
            )}
            {isLoading && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.typingIndicator}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
          </div>
          <div className={styles.chatbotInput}>
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your question..."
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className={styles.sendButton}
            >
              Send
            </button>
          </div>
        </div>
      ) : (
        <button className={styles.chatbotBtn} onClick={toggleChat}>
          💬 Chat with AI
        </button>
      )}
    </div>
  );
}

// Chapter card component
function ChapterCard({ chapter }: { chapter: Chapter }) {
  return (
    <div className={styles.chapterCard}>
      <div className={styles.chapterHeader}>
        <h3 className={styles.chapterTitle}>
          <Link to={`/docs/${chapter.id}/`}>
            {chapter.title}
          </Link>
        </h3>
      </div>
      <div className={styles.chapterSummary}>
        <p>{chapter.summary}</p>
      </div>
      <div className={styles.chapterActions}>
        <Link
          className={clsx('button button--primary button--sm', styles.readButton)}
          to={`/docs/${chapter.id}/`}
        >
          Read Chapter
        </Link>
        <Link
          className={clsx('button button--outline button--sm', styles.summaryButton)}
          to={`/docs/${chapter.id}/summary`}
        >
          View Summary
        </Link>
      </div>
    </div>
  );
}

// Chapters section component
function ChaptersSection() {
  return (
    <section className={styles.chaptersSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <Heading as="h2" className={styles.sectionTitle}>
              Book Chapters
            </Heading>
            <p className={styles.sectionSubtitle}>
              Explore the complete Physical AI and Robotics textbook, chapter by chapter
            </p>
          </div>
        </div>

        <div className="row">
          {chapters.map((chapter) => (
            <div key={chapter.id} className="col col--12 col--md-6 margin-bottom--lg">
              <ChapterCard chapter={chapter} />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Physical AI and Robotics Textbook - Complete guide to embodied artificial intelligence">
      <HomepageHeader />
      <main>
        <ChaptersSection />
        <HomepageFeatures />
      </main>
      <ChatbotWidget />
    </Layout>
  );
}
