/**
 * Example page demonstrating chatbot integration
 * This can be adapted to integrate with actual textbook pages
 */

import React, { useState } from 'react';
import Chatbot from '../components/Chatbot';
import './ChatbotIntegration.css'; // We'll create this CSS file

const ChatbotIntegrationPage = () => {
  const [showChatbot, setShowChatbot] = useState(false);
  const [userId] = useState(`user_${Date.now()}`); // Simple user ID generation

  const toggleChatbot = () => {
    setShowChatbot(!showChatbot);
  };

  return (
    <div className="chatbot-integration-page">
      <header className="page-header">
        <h1>Physical AI & Humanoid Robotics Textbook</h1>
        <p>Interactive Learning Assistant</p>
      </header>

      <main className="page-content">
        <section className="textbook-content">
          <h2>Chapter 1: Introduction to Physical AI</h2>
          <p>
            Physical AI combines robotics and artificial intelligence to create embodied systems that interact with the physical world.
            Unlike traditional AI that operates in digital spaces, Physical AI must handle real-world complexities like uncertainty,
            noise, and dynamic environments.
          </p>
          <p>
            Key components of Physical AI systems include:
          </p>
          <ul>
            <li>Sensors for perception</li>
            <li>Actuators for action</li>
            <li>Control systems for decision making</li>
            <li>Learning mechanisms for adaptation</li>
          </ul>
        </section>

        <div className="content-with-chatbot">
          <section className="additional-content">
            <h3>Learning Objectives</h3>
            <ul>
              <li>Understand the fundamentals of Physical AI</li>
              <li>Identify key components of Physical AI systems</li>
              <li>Recognize applications of Physical AI in robotics</li>
            </ul>
          </section>

          <div className="chatbot-float-container">
            <button
              className={`chatbot-toggle-btn ${showChatbot ? 'active' : ''}`}
              onClick={toggleChatbot}
            >
              {showChatbot ? 'Hide Assistant' : 'Ask Assistant'}
            </button>

            {showChatbot && (
              <div className="chatbot-panel">
                <Chatbot userId={userId} />
              </div>
            )}
          </div>
        </div>
      </main>

      <aside className="related-topics">
        <h3>Related Topics</h3>
        <ul>
          <li><a href="/docs/chapter-2-robotics-foundations">Robotics Foundations</a></li>
          <li><a href="/docs/chapter-3-humanoid-systems">Humanoid Systems</a></li>
          <li><a href="/docs/chapter-4-sensors-actuators">Sensors and Actuators</a></li>
        </ul>
      </aside>
    </div>
  );
};

export default ChatbotIntegrationPage;